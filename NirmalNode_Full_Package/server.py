"""
NirmalNode - Live Backend Server & Serial Hardware Bridge
---------------------------------------------------------
Flask REST API + background serial reader + live hardware simulation.
Run:  python server.py
Then open: http://localhost:5000

Improvements v2:
  - SQLite persistence: telemetry_log.db (survives restarts)
  - Rotating file logging: nirmalnode_server.log
  - Concept drift alerting via /api/alert and /api/stats
  - Model confidence score exposed in all API responses
"""

import sys, os, time, json, random, re, math, threading, sqlite3, logging
from logging.handlers import RotatingFileHandler
import serial
import serial.tools.list_ports
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from nirmal_ml_engine import AdaptiveAIEngine, calculate_pm25_aqi


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=".")
CORS(app)

# ---------------------------------------------------------------------------
# Logging setup (rotating file, max 2 MB × 3 backups)
# ---------------------------------------------------------------------------
_log_handler = RotatingFileHandler(
    "nirmalnode_server.log", maxBytes=2 * 1024 * 1024, backupCount=3
)
_log_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))
logging.basicConfig(level=logging.INFO, handlers=[_log_handler, logging.StreamHandler()])
log = logging.getLogger("NirmalNode")

# ---------------------------------------------------------------------------
# SQLite persistence — telemetry_log.db
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "telemetry_log.db")

def _init_db():
    """Create tables if they don't exist."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT    NOT NULL,
            pm2_5       REAL,
            aqi         INTEGER,
            aqi_category TEXT,
            forecast_1h  REAL,
            purifier    INTEGER,
            champion    TEXT,
            mae         REAL,
            rmse        REAL,
            confidence  REAL,
            drift_score REAL,
            drift_flag  INTEGER,
            raw_json    TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS drift_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT    NOT NULL,
            drift_score REAL,
            drift_count INTEGER,
            champion    TEXT
        )
    """)
    con.commit()
    con.close()
    log.info(f"SQLite DB initialised at {DB_PATH}")

_init_db()

_db_lock = threading.Lock()

def _persist_telemetry(data: dict):
    """Write one telemetry record to SQLite (non-blocking via lock)."""
    ol  = data.get("online_learning", {})
    drft = data.get("drift_alert", {})
    row = (
        data.get("timestamp", time.strftime("%H:%M:%S")),
        data.get("pm2_5", 0),
        data.get("aqi", 0),
        data.get("aqi_category", ""),
        data.get("forecast_1h", 0),
        int(data.get("purifier_trigger", False)),
        ol.get("champion_short", ""),
        ol.get("mae", 0.0),
        ol.get("rmse", 0.0),
        ol.get("confidence", 0.0),
        drft.get("drift_score", 0.0),
        int(drft.get("drift_detected", False)),
        json.dumps({k: v for k, v in data.items() if not isinstance(v, (dict, list))}),
    )
    try:
        with _db_lock:
            con = sqlite3.connect(DB_PATH)
            con.execute(
                "INSERT INTO telemetry (ts,pm2_5,aqi,aqi_category,forecast_1h,"
                "purifier,champion,mae,rmse,confidence,drift_score,drift_flag,raw_json) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row
            )
            # If drift detected, also log to drift_events
            if drft.get("drift_detected"):
                con.execute(
                    "INSERT INTO drift_events (ts,drift_score,drift_count,champion) VALUES (?,?,?,?)",
                    (row[0], drft.get("drift_score", 0), drft.get("drift_count", 0), row[6])
                )
            con.commit()
            con.close()
    except Exception as exc:
        log.warning(f"DB write error: {exc}")



# ---------------------------------------------------------------------------
# Global shared state (accessed only through the data_lock)
# ---------------------------------------------------------------------------
data_lock      = threading.Lock()
ml_engine      = AdaptiveAIEngine()
latest_data    = {}
data_history   = []          # capped at 500 records
serial_port_obj = None
simulation_mode = True        # True until hardware connects
is_running      = True

# Default "placeholder" telemetry shown before first sample arrives
_DEFAULT = dict(
    connected=False, port="SIMULATION",
    timestamp="--:--:--",
    pm1_0=0, pm2_5=0, pm10=0,
    cnt0_3=0, cnt0_5=0, cnt1_0=0, cnt2_5=0, cnt5_0=0, cnt10_0=0,
    mq135_adc=0, mq136_adc=0, mics_red_adc=0, mics_nox_adc=0, mp135_adc=0,
    aqi=0, aqi_category="N/A", aqi_color="#64748b",
    forecast_1h=0, forecast_2h=0,
    forecast_aqi=0, forecast_aqi_category="N/A",
    purifier_trigger=False, purifier_status="IDLE (CLEAN)",
    online_learning=dict(samples_trained=0, mae=0.0, rmse=0.0, status="Initializing", champion="SGD+PA Blend 0.6/0.4", champion_short="M8-BLEND"),
    xai=dict(
        method="Linear Feature Contribution (LFC)",
        description="contribution_i = (0.6*w_sgd + 0.4*w_pa)_i * x_scaled_i",
        shap_available=False,
        top_features=[],
        all_features=[],
    ),
    model_arena=ml_engine.arena.leaderboard(),
)
latest_data = dict(_DEFAULT)


# ---------------------------------------------------------------------------
# Serial parser helpers
# ---------------------------------------------------------------------------
def _extract_int(text, pattern, fallback=0):
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return int(m.group(1)) if m else fallback


def parse_text_report(buf):
    """
    Parses the human-readable report printed by NirmalNode_SensorTest.ino /
    AirGuard.ino / NirmalNode_LiveAPI.ino (text mode).
    """
    sample = {"timestamp": time.strftime("%H:%M:%S")}
    sample["pm1_0"]        = _extract_int(buf, r"PM1\.0\s*:\s*(\d+)")
    sample["pm2_5"]        = _extract_int(buf, r"PM2\.5\s*:\s*(\d+)")
    sample["pm10"]         = _extract_int(buf, r"PM10\s*:\s*(\d+)")
    sample["cnt0_3"]       = _extract_int(buf, r"P>0\.3um\s*:\s*(\d+)")
    sample["cnt0_5"]       = _extract_int(buf, r"P>0\.5um\s*:\s*(\d+)")
    sample["cnt1_0"]       = _extract_int(buf, r"P>1\.0um\s*:\s*(\d+)")
    sample["cnt2_5"]       = _extract_int(buf, r"P>2\.5um\s*:\s*(\d+)")
    sample["cnt5_0"]       = _extract_int(buf, r"P>5\.0um\s*:\s*(\d+)")
    sample["cnt10_0"]      = _extract_int(buf, r"P>10um\s*:\s*(\d+)")
    sample["mq135_adc"]    = _extract_int(buf, r"MQ135[\s\S]*?ADC\s*:\s*(\d+)")
    sample["mq136_adc"]    = _extract_int(buf, r"MQ136[\s\S]*?ADC\s*:\s*(\d+)")
    sample["mics_red_adc"] = _extract_int(buf, r"RED ADC\s*:\s*(\d+)")
    sample["mics_nox_adc"] = _extract_int(buf, r"NOX ADC\s*:\s*(\d+)")
    sample["mp135_adc"]    = _extract_int(buf, r"MP135[\s\S]*?ADC\s*:\s*(\d+)")
    return sample


def parse_json_line(line):
    """Parses a single JSON line (NirmalNode_LiveAPI JSON mode)."""
    line = line.strip()
    if not (line.startswith("{") and line.endswith("}")):
        return None
    try:
        d = json.loads(line)
        d.setdefault("timestamp", time.strftime("%H:%M:%S"))
        return d
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Telemetry update (called from any thread)
# ---------------------------------------------------------------------------
def update_telemetry(raw_sample):
    global latest_data, data_history

    ai = ml_engine.process_stream_sample(raw_sample)

    merged = {**raw_sample, **ai}
    merged["connected"] = not simulation_mode
    merged["port"]      = (serial_port_obj.port
                           if serial_port_obj and not simulation_mode
                           else "SIMULATION")

    # Persist to SQLite in background (non-blocking)
    threading.Thread(target=_persist_telemetry, args=(merged,), daemon=True).start()

    # Log drift alerts
    drft = merged.get("drift_alert", {})
    if drft.get("drift_detected"):
        log.warning(
            f"[DRIFT] score={drft.get('drift_score', 0):.2f} | "
            f"champion={merged.get('online_learning', {}).get('champion_short', '?')} | "
            f"PM2.5={merged.get('pm2_5', 0)} µg/m³"
        )

    with data_lock:
        latest_data = merged
        data_history.append(merged)
        if len(data_history) > 500:
            data_history.pop(0)



# ---------------------------------------------------------------------------
# Background: serial reader thread
# ---------------------------------------------------------------------------
def serial_reader_loop(port_name, baud=115200):
    global serial_port_obj, simulation_mode, is_running
    print(f"[Serial] Connecting to {port_name} @ {baud} baud …")
    try:
        ser = serial.Serial(port_name, baud, timeout=2.0)
        serial_port_obj = ser
        simulation_mode = False
        print(f"[Serial] Connected to {port_name}")
        try:
            time.sleep(1.5)
            ser.write(b"MODE_JSON\n")
        except Exception:
            pass

        buf = ""
        while is_running and ser.is_open:
            raw = ser.readline()
            if not raw:
                continue
            line = raw.decode("ascii", errors="ignore")

            # Try JSON first (fast path for LiveAPI JSON mode)
            parsed = parse_json_line(line)
            if parsed and "pm2_5" in parsed:
                update_telemetry(parsed)
                continue

            # Accumulate text-mode report
            buf += line
            if "==============================" in line and buf.count("==============================") >= 2:
                sample = parse_text_report(buf)
                if (sample.get("pm2_5", 0) > 0 or 
                    sample.get("mq135_adc", 0) > 0 or 
                    sample.get("mics_red_adc", 0) > 0 or 
                    "pm2_5" in sample):
                    update_telemetry(sample)
                buf = ""

    except serial.SerialException as e:
        print(f"[Serial] Error on {port_name}: {e}")
    finally:
        if serial_port_obj and serial_port_obj.is_open:
            serial_port_obj.close()
        serial_port_obj = None
        simulation_mode = True
        print("[Serial] Port closed. Switching back to simulation.")


# ---------------------------------------------------------------------------
# Background: hardware simulator (realistic industrial hotspot)
# ---------------------------------------------------------------------------
def simulator_loop():
    global is_running
    step = 0
    while is_running:
        if simulation_mode:
            step += 1
            # Sinusoidal baseline with periodic welding/combustion spikes
            base  = 22.0 + 14.0 * math.sin(step * 0.08) + random.uniform(-2, 2)
            spike = 55.0 if (step % 22 in [20, 21, 0]) else 0.0
            pm25  = round(max(4.0, base + spike), 1)

            sample = dict(
                timestamp    = time.strftime("%H:%M:%S"),
                pm1_0        = int(pm25 * 0.58),
                pm2_5        = int(pm25),
                pm10         = int(pm25 * 1.45),
                cnt0_3       = int(pm25 * 48 + random.randint(-35, 35)),
                cnt0_5       = int(pm25 * 14 + random.randint(-8, 8)),
                cnt1_0       = int(pm25 * 3.5),
                cnt2_5       = int(pm25 * 0.75),
                cnt5_0       = int(pm25 * 0.18),
                cnt10_0      = int(pm25 * 0.04),
                mq135_adc    = int(1180 + pm25 * 16 + random.randint(-25, 25)),
                mq136_adc    = int(820  + pm25 * 10 + random.randint(-15, 15)),
                mics_red_adc = int(1550 + pm25 * 19 + random.randint(-30, 30)),
                mics_nox_adc = int(1020 + pm25 * 13 + random.randint(-20, 20)),
                mp135_adc    = int(1120 + pm25 * 14 + random.randint(-20, 20)),
            )
            update_telemetry(sample)
        time.sleep(2.0)


# ---------------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

@app.route("/api/status")
def api_status():
    return jsonify(dict(
        status         = "online",
        simulation_mode= simulation_mode,
        connected_port = serial_port_obj.port if serial_port_obj else None,
        total_samples  = len(data_history),
    ))

@app.route("/api/latest")
def api_latest():
    with data_lock:
        return jsonify(latest_data)

@app.route("/api/history")
def api_history():
    with data_lock:
        return jsonify(data_history)

@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    """
    ESP32 WiFi firmware POSTs here every 2 s.
    Accepts JSON sensor data, runs ML engine, responds with fan command + XAI.
    This endpoint disables simulation mode automatically.
    """
    global simulation_mode

    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid JSON"}), 400

    # Mark as real hardware — stop simulation BEFORE update_telemetry reads it
    simulation_mode = False
    body.setdefault("timestamp", time.strftime("%H:%M:%S"))

    update_telemetry(body)

    # Read result safely inside the lock
    with data_lock:
        should_trigger = latest_data.get("purifier_trigger", False)
        aqi_val        = latest_data.get("aqi", 0)
        xai_top        = latest_data.get("xai", {}).get("top_features", [])

    fan_cmd = "FAN_ON" if should_trigger else "FAN_OFF"
    print(f"[WiFi] Data received: PM2.5={body.get('pm2_5')}  AQI~{aqi_val}  {fan_cmd}")

    return jsonify({"status": "ok", "fan": fan_cmd, "aqi": aqi_val,
                    "xai_top": xai_top}), 200

@app.route("/api/ports")
def api_ports():
    ports = [
        {"port": p.device, "description": p.description, "hwid": p.hwid}
        for p in serial.tools.list_ports.comports()
    ]
    return jsonify(ports)

@app.route("/api/connect", methods=["POST"])
def api_connect():
    global simulation_mode
    body = request.get_json(silent=True) or {}
    port = body.get("port", "").strip()

    if not port or port.upper() == "SIMULATION":
        simulation_mode = True
        return jsonify({"success": True, "mode": "SIMULATION"})

    t = threading.Thread(target=serial_reader_loop, args=(port,), daemon=True)
    t.start()
    return jsonify({"success": True, "mode": "HARDWARE", "port": port})

@app.route("/api/purifier", methods=["POST"])
def api_purifier():
    """Send FAN_ON / FAN_OFF command to connected ESP32."""
    body  = request.get_json(silent=True) or {}
    state = body.get("state", "off").lower()
    cmd   = "FAN_ON\n" if state == "on" else "FAN_OFF\n"
    if serial_port_obj and serial_port_obj.is_open:
        try:
            serial_port_obj.write(cmd.encode("ascii"))
            return jsonify({"success": True, "command": cmd.strip()})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "No serial port connected"}), 400

@app.route("/api/explain")
def api_explain():
    """XAI endpoint: global feature importance + last local contributions."""
    with data_lock:
        xai_data = latest_data.get("xai", {})
    global_imp = ml_engine.get_global_importance()
    return jsonify({
        "global_importance": global_imp,
        "local_contributions": xai_data.get("all_features", []),
        "method":  xai_data.get("method", "Linear Feature Contribution (LFC)"),
        "description": xai_data.get("description", ""),
        "shap_available": xai_data.get("shap_available", False),
        "samples_trained": ml_engine.n_samples,
    })

@app.route("/api/model_arena")
def api_model_arena():
    """Model arena leaderboard — all 9 models with prequential MAE/RMSE."""
    leaderboard = ml_engine.arena.leaderboard()
    champ = ml_engine.arena.models[ml_engine.arena.champion_idx]
    return jsonify({
        "leaderboard":    leaderboard,
        "champion":       champ.name,
        "champion_short": champ.short,
        "election_count": ml_engine.arena.election_count,
        "warmup_samples": ml_engine.arena.WARMUP_SAMPLES,
        "samples_trained":ml_engine.n_samples,
    })

@app.route("/api/export")
def api_export():
    """Download collected telemetry as CSV (for thesis Chapter 4)."""
    with data_lock:
        rows = list(data_history)

    if not rows:
        return "No data yet.", 204

    # Flatten nested 'online_learning' dict into columns
    flat_rows = []
    for r in rows:
        flat = {k: v for k, v in r.items() if not isinstance(v, dict)}
        ol = r.get("online_learning", {})
        flat["ml_samples"]  = ol.get("samples_trained", 0)
        flat["ml_mae"]      = ol.get("mae", 0.0)
        flat["ml_rmse"]     = ol.get("rmse", 0.0)
        flat["ml_status"]   = ol.get("status", "")
        flat_rows.append(flat)

    headers = list(flat_rows[0].keys())
    lines   = [",".join(str(h) for h in headers)]
    for row in flat_rows:
        lines.append(",".join(str(row.get(h, "")) for h in headers))

    csv_text = "\n".join(lines)
    return csv_text, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=nirmalnode_thesis_data.csv",
    }


@app.route("/api/stats")
def api_stats():
    """
    Session summary + SQLite database statistics.
    Useful for the thesis Chapter 4 quantitative results.
    """
    # In-memory session stats
    with data_lock:
        n = len(data_history)
        avg_pm25 = (sum(r.get("pm2_5", 0) for r in data_history) / n) if n else 0
        avg_aqi  = (sum(r.get("aqi", 0) for r in data_history) / n) if n else 0
        purifier_on = sum(1 for r in data_history if r.get("purifier_trigger")) if n else 0

    # SQLite stats
    try:
        with _db_lock:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            db_total     = cur.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
            db_drift_ev  = cur.execute("SELECT COUNT(*) FROM drift_events").fetchone()[0]
            db_avg_pm25  = cur.execute("SELECT AVG(pm2_5) FROM telemetry").fetchone()[0] or 0
            db_avg_aqi   = cur.execute("SELECT AVG(aqi) FROM telemetry").fetchone()[0] or 0
            db_avg_conf  = cur.execute("SELECT AVG(confidence) FROM telemetry").fetchone()[0] or 0
            con.close()
    except Exception:
        db_total = db_drift_ev = db_avg_pm25 = db_avg_aqi = db_avg_conf = 0

    return jsonify({
        "session": {
            "samples":        n,
            "avg_pm25":       round(avg_pm25, 2),
            "avg_aqi":        round(avg_aqi, 2),
            "purifier_on_count": purifier_on,
            "ml_samples":     ml_engine.n_samples,
            "champion_mae":   round(ml_engine.mae, 4),
            "champion_rmse":  round(ml_engine.rmse, 4),
        },
        "database": {
            "total_records":   db_total,
            "drift_events":    db_drift_ev,
            "avg_pm25":        round(db_avg_pm25, 2),
            "avg_aqi":         round(db_avg_aqi, 2),
            "avg_confidence":  round(db_avg_conf, 3),
            "db_path":         DB_PATH,
        },
        "drift": ml_engine.arena.drift.to_dict(),
    })


@app.route("/api/alert")
def api_alert():
    """
    Return recent concept drift events from SQLite.
    Query param: ?limit=N (default 20)
    """
    limit = min(int(request.args.get("limit", 20)), 200)
    try:
        with _db_lock:
            con = sqlite3.connect(DB_PATH)
            rows = con.execute(
                "SELECT ts, drift_score, drift_count, champion FROM drift_events "
                "ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            con.close()
        events = [{"ts": r[0], "drift_score": r[1],
                   "drift_count": r[2], "champion": r[3]} for r in rows]
    except Exception as exc:
        events = []
        log.warning(f"alert query error: {exc}")

    current_drift = ml_engine.arena.drift.to_dict()
    return jsonify({
        "current": current_drift,
        "recent_events": events,
        "total_events": len(events),
    })


@app.route("/api/db_export")
def api_db_export():
    """Download ALL persisted telemetry from SQLite as CSV (full history)."""
    try:
        with _db_lock:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            rows = cur.execute(
                "SELECT id,ts,pm2_5,aqi,aqi_category,forecast_1h,purifier,"
                "champion,mae,rmse,confidence,drift_score,drift_flag "
                "FROM telemetry ORDER BY id"
            ).fetchall()
            con.close()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    if not rows:
        return "No data in database yet.", 204

    header = "id,ts,pm2_5,aqi,aqi_category,forecast_1h,purifier," \
             "champion,mae,rmse,confidence,drift_score,drift_flag"
    csv_lines = [header] + [",".join(str(v) for v in row) for row in rows]
    csv_text  = "\n".join(csv_lines)
    return csv_text, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=nirmalnode_db_export.csv",
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 57)
    print("  NirmalNode – Adaptive AI & Green IoT Air Quality System")
    print("=" * 57)

    # Start simulator thread (always running; only fires when simulation_mode=True)
    threading.Thread(target=simulator_loop, daemon=True).start()

    # Auto-detect hardware
    ports = serial.tools.list_ports.comports()
    if ports:
        chosen = ports[0].device
        print(f"[AUTO] Hardware detected on {chosen}. Connecting …")
        threading.Thread(target=serial_reader_loop, args=(chosen,), daemon=True).start()
    else:
        print("[INFO] No COM port detected. Running in Demo Simulation Mode.")
        print("[INFO] Plug in your ESP32, then click 'Connect ESP32 Hardware' in the dashboard.")

    print("\n  Dashboard -> http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
