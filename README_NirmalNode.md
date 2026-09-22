# NirmalNode – Live IoT Air Quality & Adaptive AI System

Welcome to **NirmalNode**, a Green IoT and Adaptive AI-Assisted Local Air Purification & Pollution Prediction System.

---

## 🎬 Project Demo Video

[![NirmalNode Demo Video](https://img.youtube.com/vi/-UmP3GxATWU/maxresdefault.jpg)](https://youtu.be/-UmP3GxATWU)

> 🔗 **Watch on YouTube:** [https://youtu.be/-UmP3GxATWU](https://youtu.be/-UmP3GxATWU)

---

## 🚀 Quick Start Guide

### Option 1: Direct USB Web Browser Connection (Zero Setup!)
1. Plug your **ESP32 / ESP32-S3** microcontroller into your PC using a USB cable.
2. Open **Google Chrome** or **Microsoft Edge** and double-click `index.html` (or open `http://localhost:5000` if python server is running).
3. Click the **"Connect ESP32 Hardware"** button in the top header.
4. Select your ESP32 COM port and click **Connect**.
5. Live sensor readings, EPA AQI, AI predictions, and Purifier triggers will display automatically!

---

### Option 2: Run Python Backend Server (Advanced Scikit-Learn Online ML)
1. Open terminal in the project directory (`capstone 3.2`).
2. Launch the Python server:
   ```bash
   python server.py
   ```
3. Open your browser and go to: **`http://localhost:5000`**
4. The server automatically detects connected hardware COM ports or runs the **Demo Hardware Simulation** if no device is plugged in.

---

## 📊 Features & Components

1. **Adaptive Online AI Pipeline (`nirmal_ml_engine.py`)**:
   - Uses **scikit-learn `SGDRegressor` & `PassiveAggressiveRegressor`** with `partial_fit()` incremental online learning.
   - Continuously learns from streaming live data without requiring full offline retraining.
   - Predicts 1-hour and 2-hour PM2.5 concentrations and calculates official US EPA AQI.
   - Triggers pre-emptive air purification fan commands before pollution spikes occur.

2. **Real-Time Web Application (`index.html`, `style.css`, `app.js`)**:
   - **US EPA AQI Meter**: Color-coded gauge (Good -> Hazardous).
   - **Live Sensors Grid**: PM1.0, PM2.5, PM10, particle counts (>0.3µm - >10µm), MQ135, MQ136, MiCS-4514 RED/NOX, MP135.
   - **Interactive Charts (Chart.js)**: Real-time PM time-series vs 1H AI Forecast, Prequential MAE online learning loss curve.
   - **Thesis CSV Data Exporter**: Click "Export CSV" to save data logs for thesis results.

3. **ESP32 Firmware (`NirmalNode_LiveAPI.ino`)**:
   - Located inside `NirmalNode_LiveAPI/`.
   - Supports both standard Serial text output and JSON API format.
   - Controls physical relay pin (`GPIO 18`) for fan activation.
