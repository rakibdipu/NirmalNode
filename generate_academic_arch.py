# -*- coding: utf-8 -*-
"""
Generates an authentic, publication-grade academic 5-Layer Architecture Diagram
for NirmalNode without any AI cartoon graphics.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Colors
NAVY = '#1E3A8A'
TEAL = '#0F766E'
SLATE_DARK = '#0F172A'
SLATE_MUTED = '#475569'
BORDER = '#CBD5E1'

layers = [
    {
        "num": "LAYER 5",
        "name": "Actuation & Application Layer",
        "y": 80,
        "h": 14.5,
        "col": '#ECFDF5',
        "border": '#059669',
        "badge_col": '#059669',
        "modules": "Local Air Purification Train: Cyclone Pre-Separator (>10µm) • HEPA-H13 (99.97% @ 0.3µm)\nActivated Carbon Bed (VOC & Gaseous Adsorption) • 12V DC Fan Relay Actuation\nUser Interfaces: Real-Time Web Dashboard (AQI Gauge, 1h/2h Forecasts, Manual/Auto-AI Override)"
    },
    {
        "num": "LAYER 4",
        "name": "Adaptive AI & Stream Analytics Layer",
        "y": 61,
        "h": 14.5,
        "col": '#EFF6FF',
        "border": '#2563EB',
        "badge_col": '#2563EB',
        "modules": "Prequential Online Learning Engine (River & scikit-learn partial_fit) • Zero Batch Retraining\nIncremental Model Arena (9 Candidate Estimators: SGD Ridge/Huber/PA, Champion M8 Blend)\nShort-Horizon Forecasting (1–2h ahead PM2.5) • Threshold Decision Engine (Equation 3.12)\nExplainable AI (XAI) via Linear Feature Contribution (LFC / Exact SHAP) & Drift Tracking"
    },
    {
        "num": "LAYER 3",
        "name": "Transport & Cloud Storage Layer",
        "y": 42,
        "h": 14.5,
        "col": '#F8FAFC',
        "border": '#64748B',
        "badge_col": '#475569',
        "modules": "Wireless Protocol: Wi-Fi (802.11 b/g/n) • HTTP REST Ingest Endpoint (/api/ingest) & MQTT Broker\nTelemetry Packetization: Standardized JSON Payloads with Node ID, Millisecond Timestamp & Location\nCloud Ingest Backend: Python Flask Microservice • In-Memory Circular Buffer (500 records)\nPersistent Historical Logging: Time-Series SQLite Database & CSV Export Utility (/api/export)"
    },
    {
        "num": "LAYER 2",
        "name": "Edge Firmware & Signal Processing Layer",
        "y": 23,
        "h": 14.5,
        "col": '#F0FDF4',
        "border": '#16A34A',
        "badge_col": '#16A34A',
        "modules": "Edge Microcontroller: ESP32 DevKit V1 (Xtensa 32-bit Dual-Core 240MHz, FreeRTOS Core)\nDeterministic Sampling Loop: Non-blocking 2-second interrupt timer (AirGuard_WiFi.ino)\nOn-Device Signal Conditioning: Exponential Moving Average (EMA) Noise Filter (alpha = 0.25)\nCalibration Routines: Power-on clean-air baseline R0 stabilization & temperature compensation"
    },
    {
        "num": "LAYER 1",
        "name": "Physical Environmental Sensing Layer",
        "y": 4,
        "h": 14.5,
        "col": '#FEF2F2',
        "border": '#DC2626',
        "badge_col": '#DC2626',
        "modules": "Laser Particulate: Plantower PMS5003 (PM1.0, PM2.5, PM10 mass concentration + 6 bin particle counts, UART2)\nDual-Element Metal Oxide: MiCS-4514 (Reducing Gases: CO [RED pin]; Oxidizing Gases: NO2 [OX pin], ADC1)\nBroad-Spectrum Gas Sensors: MQ135 (General Air Quality: VOC, NH3, Smoke) & MP135 (Relative VOC/Solvents)\nToxic Gas Detection: MQ136 (Hydrogen Sulfide H2S / Industrial Odour) • Ambient Met: BME280 (T/H/P)"
    }
]

# Title banner inside figure
ax.text(50, 98.5, 'NirmalNode Five-Layer System Architecture', ha='center', va='center',
        fontsize=14, fontweight='bold', color=NAVY, fontfamily='sans-serif')
ax.text(50, 96.2, 'From Physical Multi-Gas Sensing to Intelligent Closed-Loop Air Purification', ha='center', va='center',
        fontsize=9, fontstyle='italic', color=SLATE_MUTED, fontfamily='sans-serif')

for lay in layers:
    # Main Layer Box
    rect = patches.FancyBboxPatch(
        (13, lay['y']), 84, lay['h'],
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor=lay['col'], edgecolor=lay['border'], linewidth=1.4
    )
    ax.add_patch(rect)
    
    # Badge Box on the Left
    badge = patches.FancyBboxPatch(
        (3, lay['y']), 8.5, lay['h'],
        boxstyle="round,pad=0.3,rounding_size=1.0",
        facecolor=lay['badge_col'], edgecolor=lay['badge_col'], linewidth=1
    )
    ax.add_patch(badge)
    
    # Layer text inside badge
    lines = lay['num'].split(' ')
    ax.text(7.25, lay['y'] + lay['h']*0.65, lines[0], ha='center', va='center',
            fontsize=8, fontweight='bold', color='white', fontfamily='sans-serif')
    ax.text(7.25, lay['y'] + lay['h']*0.35, lines[1], ha='center', va='center',
            fontsize=12, fontweight='bold', color='white', fontfamily='sans-serif')
    
    # Layer Header Title
    ax.text(15, lay['y'] + lay['h'] - 3.2, lay['name'], ha='left', va='center',
            fontsize=10.5, fontweight='bold', color=NAVY, fontfamily='sans-serif')
    
    # Divider line inside box
    ax.plot([15, 95], [lay['y'] + lay['h'] - 4.8, lay['y'] + lay['h'] - 4.8],
            color=BORDER, linewidth=0.7)
    
    # Layer Modules Details
    ax.text(15, lay['y'] + (lay['h'] - 5.2)/2, lay['modules'], ha='left', va='center',
            fontsize=7.8, color=SLATE_DARK, fontfamily='sans-serif', linespacing=1.4)

# Vertical Data Flow & Control Feedback Arrows
# Left Arrow: Telemetry Data Flow (Upward)
ax.annotate('', xy=(1.2, 88), xytext=(1.2, 10),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2, mutation_scale=15))
ax.text(1.2, 49, 'UPWARD TELEMETRY & FEATURE STREAM', ha='center', va='center',
        fontsize=7, fontweight='bold', color=NAVY, rotation=90, fontfamily='sans-serif',
        bbox=dict(boxstyle="square,pad=0.3", facecolor='white', edgecolor=NAVY, lw=0.8))

# Right Arrow: Closed-Loop Actuation Command (Downward)
ax.annotate('', xy=(98.8, 10), xytext=(98.8, 88),
            arrowprops=dict(arrowstyle="-|>", color='#059669', lw=2, mutation_scale=15))
ax.text(98.8, 49, 'CLOSED-LOOP PREDICTIVE PURIFIER TRIGGER', ha='center', va='center',
        fontsize=7, fontweight='bold', color='#059669', rotation=-90, fontfamily='sans-serif',
        bbox=dict(boxstyle="square,pad=0.3", facecolor='white', edgecolor='#059669', lw=0.8))

plt.tight_layout()
out_dir = r"c:\Users\ASUS\Downloads\capstone 3.2\figures_academic"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "five_layer_architecture_academic.png")
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.close()
print("Academic diagram generated:", out_file)
