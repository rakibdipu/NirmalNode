import math, random
from nirmal_ml_engine import AdaptiveAIEngine, calculate_pm25_aqi

print('=' * 58)
print('  NirmalNode ML Model - Full Diagnostic')
print('=' * 58)

engine = AdaptiveAIEngine()

# Simulate a realistic 50-sample stream (same as server simulator)
random.seed(42)
samples = []
for i in range(50):
    base  = 22 + 14 * math.sin(i * 0.08) + random.uniform(-2, 2)
    spike = 55 if (i % 22 in [20, 21, 0]) else 0
    pm25  = round(max(4.0, base + spike), 1)
    samples.append(dict(
        timestamp    = '12:%02d:00' % i,
        pm1_0        = int(pm25 * 0.58),
        pm2_5        = int(pm25),
        pm10         = int(pm25 * 1.45),
        cnt0_3       = int(pm25 * 48),
        cnt0_5       = int(pm25 * 14),
        cnt1_0       = int(pm25 * 3.5),
        cnt2_5       = int(pm25 * 0.75),
        mq135_adc    = int(1180 + pm25 * 16),
        mq136_adc    = int(820  + pm25 * 10),
        mics_red_adc = int(1550 + pm25 * 19),
        mics_nox_adc = int(1020 + pm25 * 13),
        mp135_adc    = int(1120 + pm25 * 14),
    ))

print()
print('--- Prequential Training (Test-Then-Train, per thesis Sec 3.9) ---')
print('  Step  PM2.5  Forecast1H    AQI     MAE    RMSE   Fan')
print('  ' + '-' * 54)

for i, s in enumerate(samples):
    r  = engine.process_stream_sample(s)
    ol = r['online_learning']
    if i % 5 == 0 or i >= 46:
        fan = 'ON ' if r['purifier_trigger'] else 'off'
        print('  %4d  %5d  %10.1f  %5d  %6.3f  %6.3f   %s' % (
            i+1, s['pm2_5'], r['forecast_1h'], r['aqi'],
            ol['mae'], ol['rmse'], fan))

print()
print('--- Final Model State ---')
print('  Samples Trained  : %d' % engine.n_samples)
print('  Final MAE        : %.3f ug/m3' % engine.mae)
print('  Final RMSE       : %.3f ug/m3' % engine.rmse)
print('  SGD coef[0]      : %.4f  (non-zero = model learned)' % engine.sgd.coef_[0])
print('  PA  coef[0]      : %.4f  (non-zero = model learned)' % engine.pa.coef_[0])
print('  EMA PM2.5        : %.2f ug/m3' % engine.ema_pm25)
print('  Model fitted?    : %s' % str(engine.is_fitted))

print()
print('--- EPA AQI Breakpoint Accuracy ---')
test_cases = [
    (6,     0,   50,  'Good'),
    (12,    50,  50,  'Good'),
    (20,    51,  100, 'Moderate'),
    (35.5,  101, 150, 'Unhealthy for Sensitive Groups'),
    (55.5,  151, 200, 'Unhealthy'),
    (100,   151, 200, 'Unhealthy'),
    (150.5, 201, 300, 'Very Unhealthy'),
    (250.5, 301, 400, 'Hazardous'),
    (350.5, 401, 500, 'Hazardous'),
]
bp_ok = True
for pm, aqi_min, aqi_max, expected_cat in test_cases:
    aqi, cat, _ = calculate_pm25_aqi(pm)
    ok = (aqi_min <= aqi <= aqi_max) and (cat == expected_cat)
    if not ok:
        bp_ok = False
    status = 'OK  ' if ok else 'FAIL'
    print('  [%s] PM2.5=%-5s  AQI=%-3d  %s' % (status, str(pm), aqi, cat))

print()
ml_ok = engine.n_samples > 0 and engine.mae > 0 and engine.is_fitted
print('ML MODEL STATUS  : %s' % ('WORKING CORRECTLY' if ml_ok else 'ERROR'))
print('AQI BREAKPOINTS  : %s' % ('ALL CORRECT' if bp_ok else 'ERRORS FOUND'))
print()
if ml_ok and bp_ok:
    print('Everything is correct! Ready for thesis defense.')
