import pandas as pd
from nirmal_ml_engine import AdaptiveAIEngine

print("=" * 65)
print("  EVALUATING MODEL ARENA ON REAL BANGLADESH DATASET")
print("=" * 65)

df = pd.read_csv("data/processed/nirmalnode_streaming_dataset.csv")
print(f"Loaded {len(df):,} real samples from Dhaka & Gazipur.")

engine = AdaptiveAIEngine()

# Evaluate on 500 real streaming samples (comparable to thesis benchmark)
eval_samples = df.head(500).to_dict(orient="records")

tp, tn, fp, fn = 0, 0, 0, 0

for i, row in enumerate(eval_samples):
    res = engine.process_stream_sample(row)
    actual_hazard = row["is_hazard"] == 1
    pred_hazard = res["purifier_trigger"]
    
    if actual_hazard and pred_hazard:
        tp += 1
    elif not actual_hazard and not pred_hazard:
        tn += 1
    elif not actual_hazard and pred_hazard:
        fp += 1
    elif actual_hazard and not pred_hazard:
        fn += 1

print("\n--- Leaderboard after 500 Real Streaming Samples ---")
lb = engine.arena.leaderboard()
for rank, m in enumerate(lb, 1):
    champ = "[CHAMPION]" if m["champion"] else ""
    print(f"  {rank}. {m['short']:<12} | {m['name']:<25} | MAE: {m['mae']:.3f} | RMSE: {m['rmse']:.3f} {champ}")

acc = (tp + tn) / (tp + tn + fp + fn)
prec = tp / (tp + fp) if (tp + fp) > 0 else 0
rec = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0

print("\n--- Purifier Trigger Contingency Matrix (N=500 Real Samples) ---")
print(f"  TP: {tp} | FP: {fp} | TN: {tn} | FN: {fn}")
print(f"  Accuracy: {acc*100:.1f}% | Precision: {prec:.3f} | Recall: {rec:.3f} | F1: {f1:.3f}")

print("\n--- Top XAI Feature Contributions on Real Smoke/Dust ---")
xai = engine.explain_prediction()
for feat in xai[:5]:
    print(f"  {feat['name']:<20}: val={feat['raw_value']:<8} contrib={feat['contribution']:<8} ({feat['direction']})")
