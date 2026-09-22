# -*- coding: utf-8 -*-
"""
Updates build_pptx_full.py to:
1. Incorporate 4 papers from 2026 on Slide 4 (Literature Review Table).
2. Replace the AI-generated 5-layer architecture diagram with the new academic diagram on Slide 8.
"""
import re

with open(r'c:\Users\ASUS\Downloads\capstone 3.2\build_pptx_full.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace 5-layer image reference
code = code.replace(
    'get_path("extracted_figs/five_layer_architecture.png")',
    'get_path("figures_academic/five_layer_architecture_academic.png")'
)

# Replace papers table data in Slide 4
old_papers = '''papers = [
    ("Alam et al. (JARSET)", "2025", "Fixed IoT node developing areas", "No", "No", "Static", "Observation only; no prediction or physical action"),
    ("Ramadhani et al. (IEEE IAICT)", "2025", "Low-cost sensor IoT air monitoring", "No", "No", "Static", "Alert threshold only; lacks predictive automation"),
    ("Pavan et al. (IJSREM)", "2025", "IoT with buzzer & SMS alerts", "No", "No", "Static", "Reactive alert; zero physical cleaner coupling"),
    ("Shabbir et al. (Env. Int.)", "2025", "Low-cost sensor review in dev. nations", "Mixed", "No", "Static", "Reviews sensing challenges; no integrated action"),
    ("Ali et al. (Air Qual. Atmos.)", "2025", "Long-term PM2.5 hotspots in Bangladesh", "No", "No", "N/A", "Satellite mapping; lacks real-time worker intervention"),
    ("Basak et al. (J. Agrofor. Env.)", "2025", "Spatial PM2.5/PM10 Tejgaon Dhaka", "No", "No", "N/A", "Quantifies exposure; proposes no engineering mitigation"),
    ("Aurnab & Khanam (WAS Poll.)", "2026", "Landfill gas emission/dispersion in Dhaka", "No", "No", "Static", "Dispersion model only; no localized worker protection"),
    ("Ghosh et al. (Heliyon)", "2026", "Atmospheric CO₂ remote sensing over BD", "No", "No", "N/A", "Macro observation; disconnected from localized action"),
    ("NirmalNode (This Work)", "2026", "Hotspot Green IoT + Adaptive AI Purifier", "Yes (1-2h)", "Yes (Pred.)", "Incremental", "First closed-loop, adaptive, pre-emptive hotspot system ($67)")
]'''

new_papers = '''papers = [
    ("Alam et al. (JARSET)", "2025", "Fixed IoT node developing areas", "No", "No", "Static", "Observation only; no prediction or physical action"),
    ("Ramadhani et al. (IEEE IAICT)", "2025", "Low-cost sensor IoT air monitoring", "No", "No", "Static", "Alert threshold only; lacks predictive automation"),
    ("Ali et al. (Air Qual. Atmos.)", "2025", "Long-term PM2.5 hotspots in Bangladesh", "No", "No", "N/A", "Satellite mapping; lacks real-time worker intervention"),
    ("Basak et al. (J. Agrofor. Env.)", "2025", "Spatial PM2.5/PM10 Tejgaon Dhaka", "No", "No", "N/A", "Quantifies exposure; proposes no engineering mitigation"),
    ("Aurnab & Khanam (WAS Poll.)", "2026", "Landfill gas emission/dispersion in Dhaka", "No", "No", "Static", "Dispersion model only; no localized worker protection"),
    ("Ghosh et al. (Heliyon)", "2026", "Atmospheric CO₂ remote sensing over BD", "No", "No", "N/A", "Macro observation; disconnected from localized action"),
    ("Jaegle (EngRxiv)", "2026", "Innovative particulate filtration technologies", "No", "Yes (Mat.)", "Static", "Filter materials evaluation; lacks sensor-AI closed-loop"),
    ("Kabir et al. (Pollution)", "2026", "PM2.5 mortality & economic loss in 6 BD cities", "Statistical", "No", "N/A", "Macro public health loss ($23B); no hotspot mitigation"),
    ("NirmalNode (This Work)", "2026", "Hotspot Green IoT + Adaptive AI Purifier", "Yes (1-2h)", "Yes (Pred.)", "Incremental", "First closed-loop, adaptive, pre-emptive hotspot system ($67)")
]'''

code = code.replace(old_papers, new_papers)

# Update row highlighting in Slide 4: indices 4, 5, 6, 7 are 2026 papers (rows 5, 6, 7, 8)
code = code.replace(
    'if r in [6, 7]: # 2026 papers',
    'if r in [4, 5, 6, 7]: # 4 papers from 2026'
)

with open(r'c:\Users\ASUS\Downloads\capstone 3.2\build_pptx_full.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_pptx_full.py successfully.")
