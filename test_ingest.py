import urllib.request, json, time

time.sleep(2)   # Wait for server to start

payload = json.dumps({
    'pm1_0': 18, 'pm2_5': 32, 'pm10': 47,
    'cnt0_3': 1540, 'cnt0_5': 450, 'cnt1_0': 110, 'cnt2_5': 25,
    'cnt5_0': 6, 'cnt10_0': 1,
    'mq135_adc': 1870, 'mq136_adc': 1240,
    'mics_red_adc': 2100, 'mics_nox_adc': 1580, 'mp135_adc': 1720,
    'co2_est': 412.5, 'co_est': 3.2, 'no2_est': 0.08,
    'pms_ok': True, 'cal_ok': True, 'fan': False
}).encode()

req = urllib.request.Request(
    'http://localhost:5000/api/ingest',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
r = urllib.request.urlopen(req)
resp = json.loads(r.read())
print('=== /api/ingest Test ===')
print('Response  :', resp)
print('Fan cmd   :', resp.get('fan'))
print('AQI       :', resp.get('aqi'))
print('Status    :', resp.get('status'))
print()
print('SUCCESS! ESP32 WiFi POST works!')
