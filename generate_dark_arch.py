# -*- coding: utf-8 -*-
"""
Generates a dark-themed, publication-grade academic 5-Layer Architecture Diagram
for NirmalNode tailored for the Z.ai / dark aesthetic.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300, facecolor='#0B0C10')
ax.set_facecolor('#0B0C10')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Dark theme palette
CYAN = '#00F0FF'
WHITE = '#F8FAFC'
OFF_WHITE = '#E2E8F0'
MUTED = '#94A3B8'
DARK_CARD = '#12141A'

layers = [
    {
        "num": "05",
        "tag": "LAYER 05",
        "name": "Actuation & Local Air Purification",
        "y": 80,
        "h": 14.5,
        "border": '#00DC82',
        "badge_bg": '#063B26',
        "badge_fg": '#00DC82',
        "modules": "Local Air Purification Train: Cyclone Pre-Separator (>10µm) • HEPA-H13 (99.97% @ 0.3µm)\nActivated Carbon Bed (VOC & Gaseous Adsorption) • 12V DC High-Speed Fan Relay Actuation\nUser Interfaces: Real-Time Web Dashboard (AQI Gauge, 1h/2h AI Forecasts, Auto/Manual Override)"
    },
    {
        "num": "04",
        "tag": "LAYER 04",
        "name": "Adaptive AI & Streaming Analytics Engine",
        "y": 61,
        "h": 14.5,
        "border": '#38BDF8',
        "badge_bg": '#0C2A4A',
        "badge_fg": '#38BDF8',
        "modules": "Prequential Online Learning Engine (River & scikit-learn partial_fit) • Zero Batch Retraining\nIncremental Model Arena (9 Candidate Estimators: SGD Ridge/Huber/PA, Champion M8 Blend)\nShort-Horizon Forecasting (1–2h ahead PM2.5) • Closed-Loop Threshold Decision Engine (Eq. 3.12)\nExplainable AI (XAI) via Linear Feature Contribution (LFC / Exact SHAP) & Drift Tracking"
    },
    {
        "num": "03",
        "tag": "LAYER 03",
        "name": "Transport & Cloud Storage Layer",
        "y": 42,
        "h": 14.5,
        "border": '#818CF8',
        "badge_bg": '#1E1B4B',
        "badge_fg": '#A5B4FC',
        "modules": "Wireless Protocol: Wi-Fi (802.11 b/g/n) • HTTP REST Ingest Endpoint (/api/ingest) & MQTT Broker\nTelemetry Packetization: Standardized JSON Payloads with Node ID, Millisecond Timestamp & Location\nCloud Ingest Backend: Python Flask Microservice • In-Memory Circular Buffer (500 records)\nPersistent Historical Logging: Time-Series SQLite Database & CSV Export Utility (/api/export)"
    },
    {
        "num": "02",
        "tag": "LAYER 02",
        "name": "Edge Firmware & Signal Processing Layer",
        "y": 23,
        "h": 14.5,
        "border": '#10B981',
        "badge_bg": '#064E3B',
        "badge_fg": '#34D399',
        "modules": "Edge Microcontroller: ESP32 DevKit V1 (Xtensa 32-bit Dual-Core 240MHz, FreeRTOS Core)\nDeterministic Sampling Loop: Non-blocking 2-second interrupt timer (AirGuard_WiFi.ino)\nOn-Device Signal Conditioning: Exponential Moving Average (EMA) Noise Filter (alpha = 0.25)\nCalibration Routines: Power-on clean-air baseline R0 stabilization & temperature compensation"
    },
    {
        "num": "01",
        "tag": "LAYER 01",
        "name": "Physical Environmental Sensing Layer",
        "y": 4,
        "h": 14.5,
        "border": '#F43F5E',
        "badge_bg": '#4C0519',
        "badge_fg": '#FB7185',
        "modules": "Laser Particulate: Plantower PMS5003 (PM1.0, PM2.5, PM10 mass concentration + 6 bin particle counts, UART2)\nDual-Element Metal Oxide: MiCS-4514 (Reducing Gases: CO [RED pin]; Oxidizing Gases: NO2 [OX pin], ADC1)\nBroad-Spectrum Gas Sensors: MQ135 (General Air Quality: VOC, NH3, Smoke) & MP135 (Relative VOC/Solvents)\nToxic Gas Detection: MQ136 (Hydrogen Sulfide H2S / Industrial Odour) • Ambient Met: BME280 (T/H/P)"
    }
]

# Header title
ax.text(50, 98.2, 'NIRMALNODE FIVE-LAYER SYSTEM ARCHITECTURE', ha='center', va='center',
        fontsize=13, fontweight='bold', color=WHITE, fontfamily='sans-serif')
ax.text(50, 95.8, 'Physical Multi-Gas Acquisition  ➔  Edge Signal Processing  ➔  Streaming AI  ➔  Closed-Loop Physical Action',
        ha='center', va='center', fontsize=8.5, color=CYAN, fontfamily='sans-serif')

for lay in layers:
    # Main Layer Box
    rect = patches.FancyBboxPatch(
        (13, lay['y']), 84, lay['h'],
        boxstyle="round,pad=0.4,rounding_size=0.8",
        facecolor=DARK_CARD, edgecolor=lay['border'], linewidth=1.2
    )
    ax.add_patch(rect)
    
    # Badge Box on the Left
    badge = patches.FancyBboxPatch(
        (3.5, lay['y']), 8, lay['h'],
        boxstyle="round,pad=0.3,rounding_size=0.6",
        facecolor=lay['badge_bg'], edgecolor=lay['border'], linewidth=1
    )
    ax.add_patch(badge)
    
    ax.text(7.5, lay['y'] + lay['h']*0.68, lay['tag'], ha='center', va='center',
            fontsize=7, fontweight='bold', color=lay['badge_fg'], fontfamily='sans-serif')
    ax.text(7.5, lay['y'] + lay['h']*0.36, lay['num'], ha='center', va='center',
            fontsize=13, fontweight='bold', color=WHITE, fontfamily='sans-serif')
    
    # Layer Title
    ax.text(15.5, lay['y'] + lay['h'] - 3.2, lay['name'], ha='left', va='center',
            fontsize=10.5, fontweight='bold', color=WHITE, fontfamily='sans-serif')
    
    # Divider line
    ax.plot([15.5, 94.5], [lay['y'] + lay['h'] - 4.8, lay['y'] + lay['h'] - 4.8],
            color='#1E222D', linewidth=0.8)
    
    # Layer Modules Details
    ax.text(15.5, lay['y'] + (lay['h'] - 5.2)/2, lay['modules'], ha='left', va='center',
            fontsize=8, color=OFF_WHITE, fontfamily='sans-serif', linespacing=1.4)

# Vertical Data Flow & Control Feedback Arrows
ax.annotate('', xy=(1.8, 88), xytext=(1.8, 10),
            arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=1.5, mutation_scale=12))
ax.text(1.8, 49, 'UPWARD TELEMETRY STREAM', ha='center', va='center',
        fontsize=6.5, fontweight='bold', color=CYAN, rotation=90, fontfamily='sans-serif')

ax.annotate('', xy=(98.2, 10), xytext=(98.2, 88),
            arrowprops=dict(arrowstyle="-|>", color='#00DC82', lw=1.5, mutation_scale=12))
ax.text(98.2, 49, 'CLOSED-LOOP PURIFIER TRIGGER', ha='center', va='center',
        fontsize=6.5, fontweight='bold', color='#00DC82', rotation=-90, fontfamily='sans-serif')

out_dir = r"c:\Users\ASUS\Downloads\capstone 3.2\figures_academic"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "five_layer_architecture_dark.png")
plt.savefig(out_file, dpi=300, facecolor='#0B0C10', bbox_inches='tight')
plt.close()
print("Dark academic diagram generated:", out_file)
