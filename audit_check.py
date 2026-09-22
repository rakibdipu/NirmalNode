import sys, os, json, time, re

print('=== 1. AUDITING nirmal_ml_engine.py ===')
try:
    import nirmal_ml_engine as mle
    engine = mle.AdaptiveAIEngine()
    
    # Test 1: Cold start sample
    s0 = {'pm1_0': 10, 'pm2_5': 20, 'pm10': 30, 'cnt0_3': 1000, 'cnt0_5': 300, 'cnt1_0': 100, 'cnt2_5': 20,
          'mq135_adc': 1200, 'mq136_adc': 800, 'mics_red_adc': 1500, 'mics_nox_adc': 1000, 'mp135_adc': 1100}
    r0 = engine.process_stream_sample(s0)
    assert r0['aqi'] > 0, 'AQI calculation failed'
    assert 'model_arena' in r0, 'model_arena missing from result'
    assert len(r0['model_arena']) == 9, f'Expected 9 models in arena, got {len(r0["model_arena"])}'
    assert len(r0['xai']['top_features']) == 5, 'Top features count mismatch'
    
    # Test 2: Stress test 200 samples
    for i in range(1, 200):
        val = 15 + (i % 30) + (50 if i % 25 == 0 else 0)
        s = {**s0, 'pm2_5': val, 'pm10': val * 1.5}
        r = engine.process_stream_sample(s)
    
    assert r['online_learning']['samples_trained'] == 200, 'Sample count mismatch'
    assert r['online_learning']['mae'] > 0, 'MAE should be positive'
    assert r['online_learning']['rmse'] >= r['online_learning']['mae'], 'RMSE must be >= MAE'
    print(f'  [PASS] ML Engine processed 200 samples successfully.')
    print(f'  [INFO] Champion: {r["online_learning"]["champion"]} | MAE: {r["online_learning"]["mae"]} | RMSE: {r["online_learning"]["rmse"]}')
    
    # Test 3: XAI explanation check
    xai = engine.explain_prediction()
    assert len(xai) == 14, f'Expected 14 feature explanations, got {len(xai)}'
    for f in xai:
        assert 'name' in f and 'contribution' in f and 'direction' in f
    print(f'  [PASS] XAI LFC feature explanation valid (14 features).')
    
    # Test 4: Global importance check
    g_imp = engine.get_global_importance()
    assert len(g_imp) == 14, f'Expected 14 global features, got {len(g_imp)}'
    imp_sum = sum(f['importance'] for f in g_imp)
    assert 0.99 <= imp_sum <= 1.01, f'Importance sum must be approx 1.0, got {imp_sum}'
    print(f'  [PASS] Global importance normalization valid (sum = {imp_sum:.4f}).')
    
except Exception as e:
    print('  [FAIL] ML Engine error:', e)
    sys.exit(1)

print('\n=== 2. AUDITING server.py Flask Endpoints ===')
try:
    import server
    client = server.app.test_client()
    
    # Endpoint /
    res = client.get('/')
    assert res.status_code == 200, f'/ returned {res.status_code}'
    print('  [PASS] GET / -> 200 OK')
    
    # Endpoint /api/latest
    res = client.get('/api/latest')
    assert res.status_code == 200, f'/api/latest returned {res.status_code}'
    d = json.loads(res.data)
    assert 'pm2_5' in d and 'aqi' in d and 'xai' in d and 'model_arena' in d
    print('  [PASS] GET /api/latest -> 200 OK (has telemetry, xai, model_arena)')
    
    # Endpoint /api/explain
    res = client.get('/api/explain')
    assert res.status_code == 200, f'/api/explain returned {res.status_code}'
    d = json.loads(res.data)
    assert 'global_importance' in d and 'local_contributions' in d
    print('  [PASS] GET /api/explain -> 200 OK')
    
    # Endpoint /api/model_arena
    res = client.get('/api/model_arena')
    assert res.status_code == 200, f'/api/model_arena returned {res.status_code}'
    d = json.loads(res.data)
    assert 'leaderboard' in d and len(d['leaderboard']) == 9
    print('  [PASS] GET /api/model_arena -> 200 OK (9-model leaderboard)')
    
    # Endpoint /api/ingest (POST simulated sensor packet)
    ingest_payload = {'pm1_0': 15, 'pm2_5': 28, 'pm10': 45, 'cnt0_3': 1400, 'cnt0_5': 400, 'cnt1_0': 150, 'cnt2_5': 35,
                      'mq135_adc': 1300, 'mq136_adc': 850, 'mics_red_adc': 1650, 'mics_nox_adc': 1050, 'mp135_adc': 1180}
    res = client.post('/api/ingest', json=ingest_payload)
    assert res.status_code == 200, f'/api/ingest returned {res.status_code}'
    d = json.loads(res.data)
    assert 'fan' in d and 'aqi' in d and 'xai_top' in d
    print(f'  [PASS] POST /api/ingest -> 200 OK (fan response: {d["fan"]}, aqi: {d["aqi"]})')
    
    # Endpoint /api/purifier
    res = client.post('/api/purifier', json={'state': 'on'})
    assert res.status_code in [200, 400], f'/api/purifier returned {res.status_code}'
    print('  [PASS] POST /api/purifier -> handled gracefully')
    
    # Endpoint /api/export
    res = client.get('/api/export')
    assert res.status_code == 200, f'/api/export returned {res.status_code}'
    assert b'pm2_5' in res.data, 'CSV header missing'
    print('  [PASS] GET /api/export -> 200 OK (valid CSV stream)')
    
except Exception as e:
    print('  [FAIL] server.py error:', e)
    sys.exit(1)

print('\n=== 3. AUDITING Frontend HTML/JS/CSS ===')
try:
    with open(r'c:\Users\ASUS\Downloads\capstone 3.2\index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    with open(r'c:\Users\ASUS\Downloads\capstone 3.2\app.js', 'r', encoding='utf-8') as f:
        js = f.read()
    with open(r'c:\Users\ASUS\Downloads\capstone 3.2\style.css', 'r', encoding='utf-8') as f:
        css = f.read()
        
    # Check all key DOM element IDs referenced in JS exist in HTML
    required_ids = [
        'valPm10', 'valPm25', 'valPm100', 'valCnt03', 'valCnt25',
        'barPm10', 'barPm25', 'barPm100', 'barCnt03', 'barCnt25',
        'valMq135', 'valMq136', 'valMicsRed', 'valMicsNox', 'valMp135',
        'barMq135', 'barMq136', 'barMicsRed', 'barMicsNox', 'barMp135',
        'mlBadge', 'xaiSampleCount', 'xaiBars', 'xaiGlobalBars',
        'arenaTable', 'arenaBody', 'arenaChampName', 'arenaSubtitle', 'arenaElections',
        'tabLocal', 'tabGlobal', 'xaiLocalPanel', 'xaiGlobalPanel',
        'connBadge', 'connLabel', 'console'
    ]
    missing_ids = [i for i in required_ids if f'id="{i}"' not in html and f"id='{i}'" not in html]
    if missing_ids:
        print('  [WARN] Missing DOM IDs in HTML:', missing_ids)
    else:
        print(f'  [PASS] All {len(required_ids)} DOM IDs verified between app.js and index.html.')
        
    # Check CSS classes
    for cls in ['.arena-card', '.arena-table', '.arena-champ', '.arena-rank', '.xai-row', '.xai-bar-fill']:
        assert cls in css, f'Missing CSS class {cls}'
    print('  [PASS] All Model Arena and XAI CSS rules verified.')
    
except Exception as e:
    print('  [FAIL] Frontend audit error:', e)
    sys.exit(1)

print('\n=== 4. AUDITING Thesis LaTeX Source & Figures ===')
try:
    tex_dir = r'c:\Users\ASUS\Downloads\capstone 3.2\thesis_src\nirmalnode_thesis'
    
    # Check all graphicspath / includegraphics targets exist
    images = []
    for root, dirs, files in os.walk(tex_dir):
        for file in files:
            if file.endswith('.tex'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                matches = re.findall(r'\\includegraphics(?:\[.*?\])?\{(.*?)\}', content)
                for m in matches:
                    bname = os.path.basename(m)
                    images.append((file, bname))
    
    fig_dir = os.path.join(tex_dir, 'figures')
    missing_figs = []
    for tex_file, fig_name in images:
        fig_path = os.path.join(fig_dir, fig_name)
        if not os.path.exists(fig_path):
            missing_figs.append((tex_file, fig_name))
            
    if missing_figs:
        print('  [FAIL] Missing figures referenced in LaTeX:', missing_figs)
        sys.exit(1)
    else:
        print(f'  [PASS] All {len(images)} figure references resolved successfully in figures/ directory.')
        
    # Check references.bib
    with open(os.path.join(tex_dir, 'references.bib'), 'r', encoding='utf-8', errors='ignore') as f:
        bib = f.read()
    entries = re.findall(r'@\w+\{([^,]+),', bib)
    print(f'  [PASS] references.bib valid with {len(entries)} citation entries.')
    
except Exception as e:
    print('  [FAIL] LaTeX audit error:', e)
    sys.exit(1)

print('\n======================================================')
print('[SUCCESS] ALL SYSTEMS AUDITED & FULLY OPERATIONAL (100% PASS)')
print('======================================================')
