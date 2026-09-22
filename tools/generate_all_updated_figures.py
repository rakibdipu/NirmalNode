import os, sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, auc, precision_recall_curve

# Matplotlib styling for academic publication
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 1.0

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nirmal_ml_engine import AdaptiveAIEngine, calculate_pm25_aqi, FEATURE_NAMES

def generate_figures():
    print("=" * 65)
    print("  GENERATING UPDATED PUBLICATION FIGURES (REAL BANGLADESH DATA)")
    print("=" * 65)

    stream_path = "data/processed/bangladesh_mendeley_dhaka_stream.csv"
    if not os.path.exists(stream_path):
        print(f"Error: {stream_path} does not exist. Run tools/train_and_evaluate_real.py first.")
        return

    df = pd.read_csv(stream_path)
    print(f"Loaded {len(df)} samples from {stream_path}")

    engine = AdaptiveAIEngine()
    N = 500

    rolling_maes = []
    rolling_rmses = []
    y_trues = []
    y_preds = []
    haz_trues = []
    haz_scores = []
    residuals = []

    conf_tp = 0
    conf_tn = 0
    conf_fp = 0
    conf_fn = 0

    for i in range(N):
        sample = df.iloc[i].to_dict()
        res = engine.process_stream_sample(sample)
        
        y_val = float(sample["pm2_5"])
        pred_val = float(res["forecast_1h"])
        is_haz = int(sample["is_hazard"])
        pred_haz = res["purifier_trigger"]

        y_trues.append(y_val)
        y_preds.append(pred_val)
        haz_trues.append(is_haz)
        
        # Soft risk score (continuous forecast normalized by threshold)
        soft_score = 1.0 / (1.0 + math.exp(-0.15 * (pred_val - 35.5)))
        haz_scores.append(soft_score)
        
        err = y_val - pred_val
        residuals.append(err)

        ol = res["online_learning"]
        rolling_maes.append(ol["mae"])
        rolling_rmses.append(ol["rmse"])

        if is_haz and pred_haz: conf_tp += 1
        elif not is_haz and not pred_haz: conf_tn += 1
        elif not is_haz and pred_haz: conf_fp += 1
        elif is_haz and not pred_haz: conf_fn += 1

    y_trues = np.array(y_trues)
    y_preds = np.array(y_preds)
    haz_trues = np.array(haz_trues)
    haz_scores = np.array(haz_scores)
    residuals = np.array(residuals)

    lb = engine.arena.leaderboard()
    print("Arena Leaderboard:")
    for m in lb:
        print(f"  {m['short']:<10}: MAE={m['mae']:.3f}, RMSE={m['rmse']:.3f}, Champ={m['champion']}")

    out_dirs = ["thesis_upgraded/figures", "journal_nirmalnode/figures"]
    for od in out_dirs:
        os.makedirs(od, exist_ok=True)

    def save_fig_all(fig, name):
        for od in out_dirs:
            p = os.path.join(od, name)
            fig.savefig(p, dpi=300, bbox_inches="tight")
        print(f"  [+] Saved {name}")

    # -------------------------------------------------------------
    # 1. Figure: model_arena_comparison.png
    # -------------------------------------------------------------
    print("\n[1/6] Rendering model_arena_comparison.png...")
    model_order = [
        ("M1: Ridge (SGD)", "M1-SGD-L2"),
        ("M2: Lasso (SGD)", "M2-SGD-L1"),
        ("M3: Elastic (SGD)", "M3-SGD-EN"),
        ("M4: Huber (SGD)", "M4-SGD-HUB"),
        ("M5: SVR (SGD)", "M5-SGD-SVR"),
        ("M6: PA (C=1.0)", "M6-PA-1"),
        ("M7: PA (C=0.1)", "M7-PA-01"),
        ("M8: Blend (SGD+PA)", "M8-BLEND"),
        ("M9: EMA (Baseline)", "M9-EMA")
    ]
    stat_dict = {m["short"]: m for m in lb}
    labels = [m[0] for m in model_order]
    maes = [stat_dict[m[1]]["mae"] for m in model_order]
    rmses = [stat_dict[m[1]]["rmse"] for m in model_order]

    # Clip very high error models visually for clear comparison if needed, or plot raw
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    x = np.arange(len(labels))
    width = 0.35

    # Colors: Highlight M6 (Champion on real data) and M8
    c_mae = ["#38bdf8" if m[1] not in ["M6-PA-1", "M8-BLEND"] else ("#f59e0b" if m[1] == "M6-PA-1" else "#fbbf24") for m in model_order]
    c_rmse = ["#0284c7" if m[1] not in ["M6-PA-1", "M8-BLEND"] else ("#d97706" if m[1] == "M6-PA-1" else "#b45309") for m in model_order]

    rects1 = ax.bar(x - width/2, maes, width, label="MAE (ug/m3)", color=c_mae, edgecolor="#1e293b", linewidth=0.8)
    rects2 = ax.bar(x + width/2, rmses, width, label="RMSE (ug/m3)", color=c_rmse, edgecolor="#1e293b", linewidth=0.8)

    ax.set_ylabel("Prediction Error (ug/m3)", fontsize=12, fontweight="bold")
    ax.set_title("Prequential Forecasting Accuracy Comparison Across 9 Incremental Models\n(Evaluated on Real-World Bangladesh Atmospheric Stream, N = 500)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.5, fontweight="bold", rotation=15, ha="right")
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=10.5, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylim(0, max(max(maes), max(rmses)) * 1.15)

    # Add text labels on top of bars
    for r1, r2, m in zip(rects1, rects2, model_order):
        h1 = r1.get_height()
        h2 = r2.get_height()
        ax.annotate(f"{h1:.1f}", xy=(r1.get_x() + r1.get_width() / 2, h1), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
        ax.annotate(f"{h2:.1f}", xy=(r2.get_x() + r2.get_width() / 2, h2), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    # Annotation callout box pointing to Champion M6
    champ_x = 5
    champ_mae = stat_dict["M6-PA-1"]["mae"]
    ax.annotate(f"Champion M6 (PA C=1.0)\nLowest MAE ({champ_mae:.2f} ug/m3)",
                xy=(champ_x - width/2, champ_mae), xytext=(champ_x - 1.2, champ_mae + 25),
                arrowprops=dict(facecolor="#b45309", edgecolor="#b45309", width=2, headwidth=8),
                bbox=dict(boxstyle="round,pad=0.4", fc="#fef3c7", ec="#f59e0b", lw=1.5),
                fontsize=10, fontweight="bold", color="#92400e")

    plt.tight_layout()
    save_fig_all(fig, "model_arena_comparison.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # 2. Figure: confusion_matrix.png
    # -------------------------------------------------------------
    print("\n[2/6] Rendering confusion_matrix.png...")
    fig, ax = plt.subplots(figsize=(7.5, 6.2), dpi=300)
    cm_matrix = np.array([[conf_tp, conf_fn],
                          [conf_fp, conf_tn]])
    
    im = ax.imshow(cm_matrix, interpolation="nearest", cmap=plt.cm.Blues)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Sample Count", rotation=-90, va="bottom", fontsize=11, fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Hazard (PM2.5 >= 35.5)", "Safe (PM2.5 < 35.5)"], fontsize=11, fontweight="bold")
    ax.set_yticklabels(["Hazard (PM2.5 >= 35.5)", "Safe (PM2.5 < 35.5)"], fontsize=11, fontweight="bold")
    ax.set_xlabel("Predicted Purifier Trigger Action", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_ylabel("Actual Field Condition", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title("Purifier Trigger Confusion Matrix (N = 500 Real Samples)\nBangladesh Air Quality Dataset", fontsize=13, fontweight="bold", pad=14)

    # Cell labels
    cells = [
        (0, 0, f"TP = {conf_tp}\n({conf_tp/N*100:.1f}%)\nTrue Hazard"),
        (0, 1, f"FN = {conf_fn}\n({conf_fn/N*100:.1f}%)\nMissed Hazard"),
        (1, 0, f"FP = {conf_fp}\n({conf_fp/N*100:.1f}%)\nFalse Alarm"),
        (1, 1, f"TN = {conf_tn}\n({conf_tn/N*100:.1f}%)\nTrue Safe")
    ]
    thresh = cm_matrix.max() / 2.0
    for r, c, txt in cells:
        val = cm_matrix[r, c]
        color = "white" if val > thresh else "#0f172a"
        ax.text(c, r, txt, ha="center", va="center", color=color, fontsize=12, fontweight="bold")

    acc = (conf_tp + conf_tn) / N
    prec = conf_tp / (conf_tp + conf_fp)
    rec = conf_tp / (conf_tp + conf_fn) if (conf_tp + conf_fn) > 0 else 1.0
    f1 = 2 * prec * rec / (prec + rec)

    # Bottom badge
    badge_text = f"Accuracy: {acc*100:.1f}%  |  Precision: {prec*100:.1f}%  |  Recall: {rec*100:.1f}%  |  F1-Score: {f1:.3f}"
    fig.text(0.5, 0.01, badge_text, ha="center", fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.5", fc="#e0f2fe", ec="#0284c7", lw=1.5), color="#0369a1")

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    save_fig_all(fig, "confusion_matrix.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # 3. Figure: prequential_error_plot.jpg
    # -------------------------------------------------------------
    print("\n[3/6] Rendering prequential_error_plot.jpg...")
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
    steps = np.arange(1, N + 1)
    
    ax.plot(steps, rolling_maes, label="Rolling MAE", color="#16a34a", linewidth=2.2)
    ax.plot(steps, rolling_rmses, label="Rolling RMSE", color="#ea580c", linewidth=2.2, linestyle="--")

    ax.set_xlabel("Sample Index (n)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Error (ug/m3)", fontsize=12, fontweight="bold")
    ax.set_title("Prequential Error Convergence on Real Bangladesh Stream\n(Online Learning Adaptation, N = 500)", fontsize=12.5, fontweight="bold", pad=12)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=11, loc="upper right")
    ax.set_ylim(0, max(rolling_rmses) * 1.1)
    ax.set_xlim(0, N)

    plt.tight_layout()
    for od in out_dirs:
        p = os.path.join(od, "prequential_error_plot.jpg")
        fig.savefig(p, dpi=300, bbox_inches="tight")
    print("  [+] Saved prequential_error_plot.jpg")
    plt.close(fig)

    # -------------------------------------------------------------
    # 4. Figure: roc_pr_curves.png
    # -------------------------------------------------------------
    print("\n[4/6] Rendering roc_pr_curves.png...")
    fpr, tpr, _ = roc_curve(haz_trues, haz_scores)
    roc_auc = auc(fpr, tpr)

    precision, recall, _ = precision_recall_curve(haz_trues, haz_scores)
    pr_auc = auc(recall, precision)
    prevalence = np.mean(haz_trues)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), dpi=300)

    # Subplot (a): ROC
    ax1.plot(fpr, tpr, color="#0284c7", lw=2.5, label=f"Model Arena (AUC = {roc_auc:.3f})")
    ax1.plot([0, 1], [0, 1], color="#94a3b8", lw=1.8, linestyle="--", label="Random Chance (AUC = 0.500)")
    ax1.set_xlim([-0.02, 1.02])
    ax1.set_ylim([-0.02, 1.05])
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("True Positive Rate (Sensitivity)", fontsize=11, fontweight="bold")
    ax1.set_title("(a) Receiver Operating Characteristic (ROC)", fontsize=12, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=10)

    # Subplot (b): PR Curve
    ax2.plot(recall, precision, color="#d97706", lw=2.5, label=f"Model Arena (PR-AUC = {pr_auc:.3f})")
    ax2.axhline(y=prevalence, color="#94a3b8", lw=1.8, linestyle="--", label=f"Baseline Prevalence ({prevalence*100:.1f}%)")
    ax2.set_xlim([-0.02, 1.02])
    ax2.set_ylim([0.2, 1.05])
    ax2.set_xlabel("Recall (Sensitivity)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Precision (Positive Predictive Value)", fontsize=11, fontweight="bold")
    ax2.set_title("(b) Precision-Recall (PR) Curve", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=10)

    plt.tight_layout()
    save_fig_all(fig, "roc_pr_curves.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # 5. Figure: residual_distribution.png
    # -------------------------------------------------------------
    print("\n[5/6] Rendering residual_distribution.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=300)

    # (a) Histogram
    n_bins = 28
    ax1.hist(residuals, bins=n_bins, density=True, color="#38bdf8", edgecolor="#0284c7", alpha=0.85)
    ax1.axvline(0, color="#ef4444", linestyle="--", lw=1.8, label="Zero Error Line")
    
    # Normal fit overlay
    mu, sigma = stats.norm.fit(residuals)
    x_grid = np.linspace(min(residuals), max(residuals), 200)
    ax1.plot(x_grid, stats.norm.pdf(x_grid, mu, sigma), color="#1e293b", lw=1.8, linestyle=":")
    
    ax1.set_xlabel("Prediction Residual (y - y_pred) [ug/m3]", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Probability Density", fontsize=11, fontweight="bold")
    ax1.set_title("(a) Forecasting Residual Error Distribution", fontsize=12, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", frameon=True, fontsize=10)

    # (b) Q-Q Plot
    (osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist="norm")
    ax2.scatter(osm, osr, color="#0284c7", s=20, alpha=0.8, edgecolors="none")
    ax2.plot(osm, slope * osm + intercept, color="#d97706", lw=2.2)
    ax2.set_xlabel("Theoretical Quantiles", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Ordered Values (ug/m3)", fontsize=11, fontweight="bold")
    ax2.set_title("(b) Residual Q-Q Plot (Normality Verification)", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    save_fig_all(fig, "residual_distribution.png")
    plt.close(fig)

    # -------------------------------------------------------------
    # 6. Figure: xai_feature_importance.png
    # -------------------------------------------------------------
    print("\n[6/6] Rendering xai_feature_importance.png...")
    g_imp = engine.get_global_importance()
    g_imp.sort(key=lambda item: item["importance"], reverse=False)

    f_names = [f["name"] for f in g_imp]
    f_vals = [f["importance"] for f in g_imp]

    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=300)
    y_pos = np.arange(len(f_names))
    
    # Colormap gradient (viridis or teal to green)
    colors = plt.cm.viridis(np.linspace(0.2, 0.85, len(f_names)))
    bars = ax.barh(y_pos, f_vals, color=colors, edgecolor="#1e293b", linewidth=0.8, height=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(f_names, fontsize=10, fontweight="bold")
    ax.set_xlabel("Normalized Global Feature Importance", fontsize=11, fontweight="bold")
    ax.set_title("Global Feature Importance of Champion Model via Linear Feature Contribution (LFC)\n(Trained on Real-World Bangladesh Multi-Pollutant Stream)", fontsize=12, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_xlim(0, max(f_vals) * 1.18)

    for bar, val in zip(bars, f_vals):
        ax.text(val + 0.003, bar.get_y() + bar.get_height() / 2, f"{val:.3f}",
                va="center", ha="left", fontsize=9, fontweight="bold", color="#0f172a")

    plt.tight_layout()
    save_fig_all(fig, "xai_feature_importance.png")
    plt.close(fig)

    print("\n" + "=" * 65)
    print("  ALL 6 FIGURES SUCCESSFULLY GENERATED & SAVED!")
    print("=" * 65)

if __name__ == "__main__":
    generate_figures()
