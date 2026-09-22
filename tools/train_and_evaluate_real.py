import os, sys
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nirmal_ml_engine import AdaptiveAIEngine, calculate_pm25_aqi

def main():
    print("=" * 65)
    print("  TRAINING & PREQUENTIAL BENCHMARK ON REAL BANGLADESH DATA")
    print("=" * 65)

    # 1. Filter Dhaka records from Mendeley/Kaggle dataset
    raw_path = "data/raw/mendeley_bangladesh_aqi_hourly_2000_2025.csv"
    print(f"[1/3] Filtering Dhaka records from {raw_path}...")
    
    dhaka_rows = []
    for chunk in pd.read_csv(raw_path, chunksize=100000):
        d = chunk[chunk["city_name"].str.lower() == "dhaka"]
        if len(d) > 0:
            dhaka_rows.append(d)

    dhaka_df = pd.concat(dhaka_rows, ignore_index=True)
    print(f"      Total Dhaka records found: {len(dhaka_df):,}")

    dhaka_df["dt"] = pd.to_datetime(dhaka_df["datetime"])
    dhaka_df = dhaka_df.sort_values("dt").reset_index(drop=True)

    # Take a 1000-sample recent chronological evaluation slice
    recent_df = dhaka_df.tail(1000).copy().reset_index(drop=True)
    t_start = recent_df["datetime"].iloc[0]
    t_end = recent_df["datetime"].iloc[-1]
    print(f"      Selected evaluation slice: 1000 samples ({t_start} to {t_end})")

    # Synthesize missing parameters (PMS5003 ratios + Gas ADC sensor responses)
    np.random.seed(42)
    stream_samples = []

    for idx, row in recent_df.iterrows():
        pm25 = float(row["pm2_5"]) if pd.notnull(row["pm2_5"]) else 30.0
        pm10 = float(row["pm10"]) if pd.notnull(row["pm10"]) else (pm25 * 1.45)
        co = float(row["carbon_monoxide"]) if pd.notnull(row["carbon_monoxide"]) else 400.0
        no2 = float(row["nitrogen_dioxide"]) if pd.notnull(row["nitrogen_dioxide"]) else 25.0
        so2 = float(row["sulphur_dioxide"]) if pd.notnull(row["sulphur_dioxide"]) else 15.0
        
        pm1_0 = round(pm25 * 0.58, 1)
        cnt0_3 = int(max(0, pm25 * 48.0 + np.random.normal(0, 10.0)))
        cnt0_5 = int(max(0, pm25 * 14.0 + np.random.normal(0, 4.0)))
        cnt1_0 = int(max(0, pm25 * 3.5 + np.random.normal(0, 1.0)))
        cnt2_5 = int(max(0, pm25 * 0.75 + np.random.normal(0, 0.3)))
        
        mq135 = int(np.clip(1150 + (co / 500.0) * 120 + pm25 * 8 + np.random.normal(0, 8), 400, 4095))
        mq136 = int(np.clip(800 + (so2 / 20.0) * 85 + pm25 * 4 + np.random.normal(0, 6), 300, 4095))
        mred  = int(np.clip(1500 + (co / 400.0) * 140 + pm25 * 10 + np.random.normal(0, 10), 500, 4095))
        mnox  = int(np.clip(1000 + (no2 / 30.0) * 95 + pm25 * 6 + np.random.normal(0, 8), 400, 4095))
        mp135 = int(np.clip(1100 + (co / 600.0) * 100 + pm25 * 7 + np.random.normal(0, 8), 400, 4095))
        
        aqi, cat, _ = calculate_pm25_aqi(pm25)
        is_hazard = (pm25 >= 35.5 or aqi > 100)
        
        stream_samples.append({
            "timestamp": row["datetime"],
            "pm1_0": pm1_0,
            "pm2_5": pm25,
            "pm10": pm10,
            "cnt0_3": cnt0_3,
            "cnt0_5": cnt0_5,
            "cnt1_0": cnt1_0,
            "cnt2_5": cnt2_5,
            "mq135_adc": mq135,
            "mq136_adc": mq136,
            "mics_red_adc": mred,
            "mics_nox_adc": mnox,
            "mp135_adc": mp135,
            "aqi": aqi,
            "aqi_category": cat,
            "is_hazard": int(is_hazard)
        })

    out_stream = "data/processed/bangladesh_mendeley_dhaka_stream.csv"
    pd.DataFrame(stream_samples).to_csv(out_stream, index=False)
    print(f"      [+] Saved processed streaming dataset: {out_stream}")

    # 2. Run Prequential Training & Tournament
    print("\n[2/3] Streaming through NirmalNode Model Arena (Prequential Protocol)...")
    engine = AdaptiveAIEngine()

    eval_n = 500
    y_trues = []
    y_preds = []
    conf_tp, conf_tn, conf_fp, conf_fn = 0, 0, 0, 0

    for i in range(eval_n):
        s = stream_samples[i]
        res = engine.process_stream_sample(s)
        y_trues.append(s["pm2_5"])
        y_preds.append(res["forecast_1h"])
        
        actual_h = (s["is_hazard"] == 1)
        pred_h   = res["purifier_trigger"]
        if actual_h and pred_h: conf_tp += 1
        elif not actual_h and not pred_h: conf_tn += 1
        elif not actual_h and pred_h: conf_fp += 1
        elif actual_h and not pred_h: conf_fn += 1

    # 3. Compute Metrics
    print("\n[3/3] FINAL BENCHMARK METRICS ON REAL BANGLADESH DATASET (N=500)")
    print("=" * 65)

    y_trues = np.array(y_trues)
    y_preds = np.array(y_preds)
    ss_res = np.sum((y_trues - y_preds) ** 2)
    ss_tot = np.sum((y_trues - np.mean(y_trues)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    lb = engine.arena.leaderboard()
    print(f"{'ID':<10} {'Model Description':<32} {'MAE':<10} {'RMSE':<10} {'Status'}")
    print("-" * 68)
    for m in lb:
        champ = "[CHAMPION]" if m["champion"] else ""
        print(f"{m['short']:<10} {m['name']:<32} {m['mae']:<10.3f} {m['rmse']:<10.3f} {champ}")

    prec = conf_tp / (conf_tp + conf_fp) if (conf_tp + conf_fp) > 0 else 0
    rec  = conf_tp / (conf_tp + conf_fn) if (conf_tp + conf_fn) > 0 else 0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    acc  = (conf_tp + conf_tn) / eval_n

    print("\n--- Hazard Contingency Matrix (Threshold PM2.5 >= 35.5 ug/m3) ---")
    print(f"  TP (True Positives)  : {conf_tp} ({conf_tp/eval_n*100:.1f}%)")
    print(f"  TN (True Negatives)  : {conf_tn} ({conf_tn/eval_n*100:.1f}%)")
    print(f"  FP (False Positives) : {conf_fp} ({conf_fp/eval_n*100:.1f}%)")
    print(f"  FN (False Negatives) : {conf_fn} ({conf_fn/eval_n*100:.1f}%)")
    print(f"  Accuracy : {acc*100:.2f}%")
    print(f"  Precision: {prec:.3f}")
    print(f"  Recall   : {rec:.3f}")
    print(f"  F1-Score : {f1:.3f}")
    print(f"  R2 Score : {r2:.4f}")

    print("\n--- Top 5 XAI Features on Real Bangladesh Air Quality ---")
    for f in engine.explain_prediction()[:5]:
        print(f"  {f['name']:<20}: {f['contribution']:+.3f} ({f['direction']})")

if __name__ == "__main__":
    main()
