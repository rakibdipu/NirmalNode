"""
NirmalNode - Adaptive AI & Online Machine Learning Pipeline
-----------------------------------------------------------
ModelArena: Prequential (test-then-train) comparison of 9 incremental
learners running in parallel on the same streaming air-quality data.
After a configurable warm-up period the Arena automatically elects the
model with the lowest cumulative MAE as the active production model.

Models evaluated (Section 3.9):
  M1  SGD – Squared Error  + L2            (Ridge online)
  M2  SGD – Squared Error  + L1            (Lasso online)
  M3  SGD – Squared Error  + ElasticNet    (combined regularisation)
  M4  SGD – Huber Loss     + L2            (robust to PM spikes)
  M5  SGD – Epsilon-Insensitive + L2       (SVR-style online)
  M6  PA  – C = 1.0                        (aggressive update)
  M7  PA  – C = 0.1                        (conservative update)
  M8  SGD+PA Blend 0.6/0.4  (M1 + M6)     (thesis champion)
  M9  EMA Baseline                         (naive benchmark)

XAI Module (Section 3.10):
  Linear Feature Contribution (LFC): contribution_i = w_i * x_scaled_i
  Equivalent to exact SHAP for linear models.
"""

import time
import math
import copy
import numpy as np
from collections import deque
from sklearn.linear_model import SGDRegressor, PassiveAggressiveRegressor
from sklearn.preprocessing import StandardScaler


# ===========================================================================
# Concept Drift Detector (ADWIN-inspired sliding window on absolute error)
# ===========================================================================
class DriftDetector:
    """
    Lightweight ADWIN-style drift detector that monitors the champion model's
    rolling absolute error.  If the short-window mean error exceeds the
    long-window mean by > DRIFT_FACTOR * σ_long the detector raises a drift
    alarm.

    Thesis Section 3.9.4 – Online Drift Monitoring.
    """

    LONG_WIN  = 60    # samples in long baseline window
    SHORT_WIN = 15    # samples in short detection window
    DRIFT_FACTOR = 2.0   # alarm when short_mean > long_mean + factor * long_std

    def __init__(self):
        self._long  = deque(maxlen=self.LONG_WIN)
        self._short = deque(maxlen=self.SHORT_WIN)
        self.drift_detected  = False
        self.drift_score     = 0.0   # z-score of short vs long window
        self.drift_count     = 0     # number of times drift was signaled

    def update(self, abs_error: float) -> bool:
        """Feed one absolute prediction error; return True if drift is detected."""
        self._long.append(abs_error)
        self._short.append(abs_error)

        if len(self._long) < self.LONG_WIN or len(self._short) < self.SHORT_WIN:
            self.drift_detected = False
            self.drift_score    = 0.0
            return False

        long_mean = float(np.mean(self._long))
        long_std  = float(np.std(self._long)) + 1e-6   # avoid /0
        short_mean = float(np.mean(self._short))

        self.drift_score = (short_mean - long_mean) / long_std
        self.drift_detected = self.drift_score > self.DRIFT_FACTOR

        if self.drift_detected:
            self.drift_count += 1

        return self.drift_detected

    def reset(self):
        """Call after champion changes to reset the short window."""
        self._short.clear()
        self.drift_detected = False
        self.drift_score    = 0.0

    def to_dict(self):
        return {
            "drift_detected":  self.drift_detected,
            "drift_score":     round(self.drift_score, 3),
            "drift_count":     self.drift_count,
            "long_window_n":   len(self._long),
            "short_window_n":  len(self._short),
        }

# Optional SHAP
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

# ===========================================================================
# Feature names (must match _build_features() order exactly — 14 features)
# ===========================================================================
FEATURE_NAMES = [
    "PM1.0",
    "PM2.5 (current)",
    "PM10",
    "Count >0.3um",
    "Count >0.5um",
    "Count >1.0um",
    "Count >2.5um",
    "MQ135 ADC",
    "MQ136 ADC",
    "MICS RED ADC",
    "MICS NOX ADC",
    "MP135 ADC",
    "PM2.5 delta(lag-1)",
    "PM2.5 EMA",
]

# ===========================================================================
# US EPA AQI Breakpoints (PM2.5 ug/m3)
# ===========================================================================
PM25_BREAKPOINTS = [
    (0.0,   12.0,   0,  50,  "Good",                            "#10b981"),
    (12.1,  35.4,  51, 100,  "Moderate",                        "#f59e0b"),
    (35.5,  55.4, 101, 150,  "Unhealthy for Sensitive Groups",  "#f97316"),
    (55.5, 150.4, 151, 200,  "Unhealthy",                       "#ef4444"),
    (150.5,250.4, 201, 300,  "Very Unhealthy",                  "#8b5cf6"),
    (250.5,350.4, 301, 400,  "Hazardous",                       "#6b21a8"),
    (350.5,500.4, 401, 500,  "Hazardous",                       "#4c1d95"),
]


def calculate_pm25_aqi(pm25):
    """Calculates US EPA AQI from PM2.5 (ug/m3)."""
    conc = math.floor(max(0.0, float(pm25)) * 10.0) / 10.0
    conc = min(conc, 500.4)
    for c_low, c_high, i_low, i_high, category, color in PM25_BREAKPOINTS:
        if c_low <= conc <= c_high:
            aqi = round(((i_high - i_low) / (c_high - c_low)) * (conc - c_low) + i_low)
            return int(aqi), category, color
    return 500, "Hazardous", "#4c1d95"


# ===========================================================================
# Single-model wrapper for prequential evaluation
# ===========================================================================
class _SingleModel:
    """
    Wraps one sklearn incremental estimator with its own scaler and
    prequential statistics.  Blend models (M8) hold TWO base estimators.
    """

    def __init__(self, name, short, model_a, model_b=None, alpha_a=1.0, alpha_b=0.0):
        self.name     = name     # full display name
        self.short    = short    # short key / badge
        self.model_a  = model_a
        self.model_b  = model_b  # second model for blends (or None)
        self.alpha_a  = alpha_a  # blend weight for model_a
        self.alpha_b  = alpha_b  # blend weight for model_b
        self.scaler   = StandardScaler()
        self.fitted   = False

        # Prequential stats
        self.n         = 0
        self.cum_abs   = 0.0
        self.cum_sq    = 0.0
        self.mae       = 0.0
        self.rmse      = 0.0

        # Last prediction (for delayed-label scoring)
        self._last_pred = None
        self._last_Xsc  = None

    def _predict_raw(self, X_sc):
        """Blended or single-model prediction on scaled features."""
        if not self.fitted:
            return 0.0
        p = self.alpha_a * self.model_a.predict(X_sc)[0]
        if self.model_b is not None:
            p += self.alpha_b * self.model_b.predict(X_sc)[0]
        return float(p)

    def predict(self, X_raw):
        """Scale features and return prediction.  Updates scaler online."""
        self.scaler.partial_fit(X_raw)
        X_sc = self.scaler.transform(X_raw)
        self._last_Xsc = X_sc
        pred = self._predict_raw(X_sc)
        self._last_pred = pred
        return pred, X_sc

    def score_and_train(self, X_raw, y_true):
        """
        Prequential step: score the PREVIOUS prediction, then partial_fit
        with the current observation.
        """
        # Scale
        self.scaler.partial_fit(X_raw)
        X_sc = self.scaler.transform(X_raw)

        # Score previous prediction if available
        if self._last_pred is not None and self.fitted:
            err = abs(y_true - self._last_pred)
            self.n       += 1
            self.cum_abs += err
            self.cum_sq  += err * err
            self.mae  = self.cum_abs / self.n
            self.rmse = math.sqrt(self.cum_sq / self.n)

        # Train: partial_fit
        y_arr = np.array([y_true])
        self.model_a.partial_fit(X_sc, y_arr)
        if self.model_b is not None:
            self.model_b.partial_fit(X_sc, y_arr)
        self.fitted = True

        # Make next prediction
        pred = self._predict_raw(X_sc)
        self._last_pred = pred
        self._last_Xsc  = X_sc
        return pred, X_sc

    def coef_blend(self):
        """Return blended coefficient vector (for XAI)."""
        if not self.fitted:
            return None
        w = self.alpha_a * self.model_a.coef_
        if self.model_b is not None:
            w = w + self.alpha_b * self.model_b.coef_
        return w

    def to_dict(self):
        # Confidence: 100% when MAE=0, ~0% when MAE >= 30 µg/m³ (typical hazard onset)
        confidence = max(0.0, round(1.0 - min(self.mae / 30.0, 1.0), 3)) if self.n > 0 else 0.0
        return {
            "name":       self.name,
            "short":      self.short,
            "n":          self.n,
            "mae":        round(self.mae,  4),
            "rmse":       round(self.rmse, 4),
            "confidence": confidence,
        }


# ===========================================================================
# EMA Baseline (naive benchmark — no sklearn model)
# ===========================================================================
class _EMABaseline:
    """Naive 1-step-ahead EMA forecast as a non-ML baseline."""

    def __init__(self, alpha=0.25):
        self.name    = "EMA Baseline (naive)"
        self.short   = "M9-EMA"
        self.alpha   = alpha
        self.ema     = None
        self.fitted  = False
        self.n       = 0
        self.cum_abs = 0.0
        self.cum_sq  = 0.0
        self.mae     = 0.0
        self.rmse    = 0.0
        self._last_pred = None
        self._last_Xsc  = None
        # Dummy coef for interface compatibility
        self.coef_   = np.zeros(len(FEATURE_NAMES))

    def predict(self, X_raw):
        pm25 = float(X_raw[0, 1])   # feature index 1 = PM2.5 current
        if self.ema is None:
            self.ema = pm25
        pred = self.ema * (1 + 0.03)  # simple 3 % growth projection
        self._last_pred = pred
        self._last_Xsc  = X_raw
        return pred, X_raw

    def score_and_train(self, X_raw, y_true):
        pm25 = float(X_raw[0, 1])
        if self.ema is None:
            self.ema = pm25
        # Score
        if self._last_pred is not None:
            err = abs(y_true - self._last_pred)
            self.n       += 1
            self.cum_abs += err
            self.cum_sq  += err * err
            self.mae  = self.cum_abs / self.n
            self.rmse = math.sqrt(self.cum_sq / self.n)
        # Update EMA
        self.ema    = self.alpha * pm25 + (1.0 - self.alpha) * self.ema
        self.fitted = True
        pred = self.ema * 1.03
        self._last_pred = pred
        self._last_Xsc  = X_raw
        return pred, X_raw

    def coef_blend(self):
        return self.coef_

    def to_dict(self):
        confidence = max(0.0, round(1.0 - min(self.mae / 30.0, 1.0), 3)) if self.n > 0 else 0.0
        return {
            "name":       self.name,
            "short":      self.short,
            "n":          self.n,
            "mae":        round(self.mae,  4),
            "rmse":       round(self.rmse, 4),
            "confidence": confidence,
        }


# ===========================================================================
# ModelArena — 9 models, parallel prequential evaluation
# ===========================================================================
class ModelArena:
    """
    Runs 9 incremental models in parallel on the same streaming data.
    After WARMUP_SAMPLES the arena elects the champion (lowest MAE).
    The champion's predictions are used for purifier decisions.

    Thesis Section 3.9.3 – Model Selection via Prequential Arena.
    """

    WARMUP_SAMPLES = 50   # minimum samples before election

    def __init__(self):
        self.models = self._build_models()
        self.champion_idx = 7   # default: M8 SGD+PA Blend (0-indexed)
        self.champion_locked = False
        self.election_count  = 0
        self.drift = DriftDetector()   # monitor champion's live error stream

    # ------------------------------------------------------------------
    def _build_models(self):
        """Instantiate all 9 model wrappers."""
        def sgd(**kw):
            return SGDRegressor(learning_rate='invscaling', eta0=0.05,
                                power_t=0.25, random_state=42,
                                max_iter=1, **kw)
        def pa(**kw):
            return PassiveAggressiveRegressor(fit_intercept=True,
                                              random_state=42,
                                              max_iter=1, **kw)

        models = [
            # M1 — SGD Squared Error + L2 (Ridge)
            _SingleModel("SGD Ridge (L2)",       "M1-SGD-L2",
                         sgd(loss='squared_error', penalty='l2', alpha=0.0001)),
            # M2 — SGD Squared Error + L1 (Lasso)
            _SingleModel("SGD Lasso (L1)",       "M2-SGD-L1",
                         sgd(loss='squared_error', penalty='l1', alpha=0.0001)),
            # M3 — SGD Squared Error + ElasticNet
            _SingleModel("SGD ElasticNet",        "M3-SGD-EN",
                         sgd(loss='squared_error', penalty='elasticnet',
                             alpha=0.0001, l1_ratio=0.5)),
            # M4 — SGD Huber + L2 (robust to outlier spikes)
            _SingleModel("SGD Huber (L2)",        "M4-SGD-HUB",
                         sgd(loss='huber',         penalty='l2', alpha=0.0001,
                             epsilon=1.35)),
            # M5 — SGD Epsilon-Insensitive + L2 (online SVR)
            _SingleModel("SGD Eps-Insensitive",   "M5-SGD-SVR",
                         sgd(loss='epsilon_insensitive', penalty='l2',
                             alpha=0.0001, epsilon=0.5)),
            # M6 — Passive Aggressive C=1.0 (aggressive)
            _SingleModel("PA Regressor C=1.0",    "M6-PA-1",
                         pa(C=1.0)),
            # M7 — Passive Aggressive C=0.1 (conservative)
            _SingleModel("PA Regressor C=0.1",    "M7-PA-01",
                         pa(C=0.1)),
            # M8 — SGD+PA Blend 0.6/0.4 (thesis champion)
            _SingleModel("SGD+PA Blend 0.6/0.4",  "M8-BLEND",
                         sgd(loss='squared_error', penalty='l2', alpha=0.0001),
                         pa(C=1.0),
                         alpha_a=0.6, alpha_b=0.4),
            # M9 — EMA Baseline (naive benchmark)
            _EMABaseline(alpha=0.25),
        ]
        return models

    # ------------------------------------------------------------------
    def _elect_champion(self):
        """
        Among models with n >= WARMUP_SAMPLES, elect the one with lowest MAE.
        Ties broken by RMSE.  Resets the drift detector when champion changes.
        """
        eligible = [(i, m) for i, m in enumerate(self.models)
                    if m.n >= self.WARMUP_SAMPLES]
        if not eligible:
            return
        best_idx = min(eligible, key=lambda im: (im[1].mae, im[1].rmse))[0]
        if best_idx != self.champion_idx:
            self.champion_idx = best_idx
            self.election_count += 1
            self.drift.reset()   # fresh drift window after champion switch

    # ------------------------------------------------------------------
    def process(self, X_raw, y_true):
        """
        Feed one sample through all models (prequential step).
        Returns champion's prediction and per-model stats.
        """
        preds = []
        for m in self.models:
            pred, _ = m.score_and_train(X_raw, y_true)
            preds.append(pred)

        # Re-elect champion every 10 samples after warmup
        if self.models[self.champion_idx].n % 10 == 0:
            self._elect_champion()

        champ = self.models[self.champion_idx]

        # Feed champion's absolute error into drift detector
        if champ._last_pred is not None:
            abs_err = abs(y_true - champ._last_pred)
            self.drift.update(abs_err)

        return float(preds[self.champion_idx]), champ

    # ------------------------------------------------------------------
    def leaderboard(self):
        """Return sorted list of model stats for display/API."""
        rows = [m.to_dict() for m in self.models]
        # Sort by MAE (models with 0 samples go last)
        rows.sort(key=lambda r: (r['mae'] if r['n'] > 0 else 9999, r['rmse']))
        # Tag champion
        champ_short = self.models[self.champion_idx].short
        for r in rows:
            r['champion'] = (r['short'] == champ_short)
        return rows

    # ------------------------------------------------------------------
    def champion_coef(self):
        return self.models[self.champion_idx].coef_blend()

    def champion_last_Xsc(self):
        return self.models[self.champion_idx]._last_Xsc


# ===========================================================================
# AdaptiveAIEngine  (main engine — wraps ModelArena + XAI)
# ===========================================================================
class AdaptiveAIEngine:
    """
    Public interface consumed by server.py.
    Delegates to ModelArena for multi-model prequential evaluation.
    Adds XAI (LFC) explanation on top of the champion model.
    """

    HAZARD_THRESHOLD = 35.5   # PM2.5 ug/m3 — purifier ON above this

    def __init__(self, history_len=120):
        self.arena   = ModelArena()
        self.history = deque(maxlen=history_len)
        self.ema_pm25  = None
        self.ema_alpha = 0.25

        # Aliases to champion stats (updated each sample)
        self.n_samples = 0
        self.mae       = 0.0
        self.rmse      = 0.0

        # XAI state
        self._last_X_sc  = None
        self._last_X_raw = None

    # ------------------------------------------------------------------
    def _build_features(self, sample):
        pm1   = float(sample.get('pm1_0',         0))
        pm25  = float(sample.get('pm2_5',         0))
        pm10  = float(sample.get('pm10',          0))
        c03   = float(sample.get('cnt0_3',        0))
        c05   = float(sample.get('cnt0_5',        0))
        c10   = float(sample.get('cnt1_0',        0))
        c25   = float(sample.get('cnt2_5',        0))
        mq135 = float(sample.get('mq135_adc',    0))
        mq136 = float(sample.get('mq136_adc',    0))
        mred  = float(sample.get('mics_red_adc', 0))
        mnox  = float(sample.get('mics_nox_adc', 0))
        mp135 = float(sample.get('mp135_adc',    0))

        # Lag-1 delta
        delta = (pm25 - float(self.history[-1].get('pm2_5', pm25))
                 if self.history else 0.0)

        # EMA
        if self.ema_pm25 is None:
            self.ema_pm25 = pm25
        else:
            self.ema_pm25 = self.ema_alpha * pm25 + (1.0 - self.ema_alpha) * self.ema_pm25

        return np.array(
            [pm1, pm25, pm10, c03, c05, c10, c25,
             mq135, mq136, mred, mnox, mp135,
             delta, self.ema_pm25],
            dtype=np.float64
        ).reshape(1, -1)

    # ------------------------------------------------------------------
    def explain_prediction(self, X_sc=None):
        """Linear Feature Contribution (LFC) — exact SHAP for linear models."""
        if X_sc is None:
            X_sc = self._last_X_sc
        if X_sc is None:
            return []

        w = self.arena.champion_coef()
        if w is None:
            return []

        X_flat  = X_sc.flatten()
        contribs = w * X_flat
        raw_vals = (self._last_X_raw.flatten()
                    if self._last_X_raw is not None else X_flat)

        result = []
        for name, contrib, raw in zip(FEATURE_NAMES, contribs, raw_vals):
            result.append({
                "name":        name,
                "raw_value":   round(float(raw),    3),
                "contribution":round(float(contrib), 4),
                "direction":   "up" if contrib >= 0 else "down",
            })
        result.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        return result

    def get_global_importance(self):
        """Normalized |w| for the champion model."""
        w = self.arena.champion_coef()
        if w is None:
            return []
        abs_w = np.abs(w)
        total = abs_w.sum() or 1.0
        normed = abs_w / total
        result = [{"name": n, "importance": round(float(v), 4)}
                  for n, v in zip(FEATURE_NAMES, normed)]
        result.sort(key=lambda x: x["importance"], reverse=True)
        return result

    def get_shap_explanation(self):
        if not SHAP_AVAILABLE:
            return {"error": "shap not installed — pip install shap"}
        return {"error": "SHAP offline batch not yet configured"}

    # ------------------------------------------------------------------
    def process_stream_sample(self, sample: dict) -> dict:
        """
        Main entry point called by server.py for each sensor record.
        Returns a rich result dict including champion prediction,
        XAI explanation, and the full arena leaderboard.
        """
        X_raw = self._build_features(sample)
        self._last_X_raw = X_raw.copy()
        pm25  = float(sample.get('pm2_5', 0))

        # --- Prequential step (all 9 models) ---
        champion_pred, champ_model = self.arena.process(X_raw, pm25)

        # Store scaled features from champion for XAI
        self._last_X_sc = champ_model._last_Xsc

        self.history.append(sample)
        self.n_samples += 1

        # Update public aliases from champion stats
        self.mae  = champ_model.mae
        self.rmse = champ_model.rmse

        # --- AQI ---
        aqi, category, color = calculate_pm25_aqi(pm25)
        fc1  = round(max(0, champion_pred), 2)
        fc2  = round(max(0, champion_pred * 1.03), 2)
        fc_aqi, fc_cat, _ = calculate_pm25_aqi(fc1)

        # --- Purifier trigger ---
        purifier = (fc1 >= self.HAZARD_THRESHOLD or aqi > 100)

        # --- Online learning stats ---
        champ_confidence = max(0.0, round(1.0 - min(champ_model.mae / 30.0, 1.0), 3))
        ol = {
            "samples_trained":    self.n_samples,
            "mae":                round(self.mae,  4),
            "rmse":               round(self.rmse, 4),
            "status": ("Warming Up"
                       if self.n_samples < ModelArena.WARMUP_SAMPLES
                       else f"Active — Champion: {champ_model.short}"),
            "champion":           champ_model.name,
            "champion_short":     champ_model.short,
            "confidence":         champ_confidence,
        }

        # --- Drift detection ---
        drift_info = self.arena.drift.to_dict()
        drift_info["description"] = (
            "⚠ Concept drift detected — model accuracy may be degraded!"
            if drift_info["drift_detected"]
            else "Stable — no concept drift detected"
        )

        # --- XAI ---
        top_features = self.explain_prediction(self._last_X_sc)
        xai = {
            "method":         "Linear Feature Contribution (LFC) — Exact SHAP",
            "champion_model": champ_model.name,
            "shap_available": SHAP_AVAILABLE,
            "top_features":   top_features[:5],
            "all_features":   top_features,
        }

        return {
            "timestamp":             time.strftime("%H:%M:%S"),
            "current_pm25":          pm25,
            "pm2_5":                 pm25,
            "pm1_0":                 sample.get('pm1_0', 0),
            "pm10":                  sample.get('pm10', 0),
            "cnt0_3":                sample.get('cnt0_3', 0),
            "cnt0_5":                sample.get('cnt0_5', 0),
            "cnt1_0":                sample.get('cnt1_0', 0),
            "cnt2_5":                sample.get('cnt2_5', 0),
            "mq135_adc":             sample.get('mq135_adc', 0),
            "mq136_adc":             sample.get('mq136_adc', 0),
            "mics_red_adc":          sample.get('mics_red_adc', 0),
            "mics_nox_adc":          sample.get('mics_nox_adc', 0),
            "mp135_adc":             sample.get('mp135_adc', 0),
            "aqi":                   aqi,
            "aqi_category":          category,
            "aqi_color":             color,
            "forecast_1h":           fc1,
            "forecast_2h":           fc2,
            "forecast_aqi":          fc_aqi,
            "forecast_aqi_category": fc_cat,
            "purifier_trigger":      purifier,
            "purifier_status":       ("ACTIVE (PRE-EMPTIVE)" if purifier else "IDLE (CLEAN)"),
            "online_learning":       ol,
            "drift_alert":           drift_info,
            "xai":                   xai,
            "model_arena":           self.arena.leaderboard(),
        }
