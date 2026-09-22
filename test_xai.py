import math, random
from nirmal_ml_engine import AdaptiveAIEngine, FEATURE_NAMES

print('=' * 60)
print('  XAI Module Test')
print('=' * 60)

engine = AdaptiveAIEngine()
random.seed(42)

# Train 30 samples
for i in range(30):
    pm25 = round(22 + 14*math.sin(i*0.08) + random.uniform(-2,2), 1)
    s = dict(pm1_0=int(pm25*0.58), pm2_5=int(pm25), pm10=int(pm25*1.45),
             cnt0_3=int(pm25*48), cnt0_5=int(pm25*14), cnt1_0=int(pm25*3.5),
             cnt2_5=int(pm25*0.75),
             mq135_adc=int(1180+pm25*16), mq136_adc=int(820+pm25*10),
             mics_red_adc=int(1550+pm25*19), mics_nox_adc=int(1020+pm25*13),
             mp135_adc=int(1120+pm25*14))
    engine.process_stream_sample(s)

# Test XAI on HIGH pollution sample
high = dict(pm1_0=45, pm2_5=78, pm10=113,
            cnt0_3=3744, cnt0_5=1092, cnt1_0=273, cnt2_5=58,
            mq135_adc=2428, mq136_adc=1600, mics_red_adc=3032,
            mics_nox_adc=2034, mp135_adc=2212)
result = engine.process_stream_sample(high)

print()
print('--- Local Contributions (HIGH pollution: PM2.5=78) ---')
xai = result.get('xai', {})
for f in xai.get('top_features', []):
    sign = '+' if f['contribution'] > 0 else ''
    arrow = 'UP  (pushes forecast HIGHER)' if f['direction'] == 'up' else 'DOWN (pushes forecast LOWER)'
    name_padded = f['name'].ljust(20)
    print('  ' + name_padded + '  ' + sign + str(round(f['contribution'],4)).ljust(8) + '  ' + arrow)

print()
print('--- Global Feature Importance ---')
gi = engine.get_global_importance()
for f in gi[:8]:
    bar = '*' * int(f['importance'] * 80)
    name_padded = f['name'].ljust(20)
    imp_str = str(round(f['importance'], 4)).ljust(7)
    w_str = ('+' if f['weight'] >= 0 else '') + str(round(f['weight'], 4))
    print('  ' + name_padded + '  imp=' + imp_str + '  w=' + w_str + '  ' + bar)

print()
print('XAI Method  :', xai.get('method'))
print('SHAP Avail  :', xai.get('shap_available'))
print('Top features:', len(xai.get('top_features', [])))
print('All features:', len(xai.get('all_features', [])))
print()
print('XAI OK:', len(xai.get('top_features', [])) == 5)
