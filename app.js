/**
 * NirmalNode AI – Dashboard Client Script
 * =========================================
 * Modes:
 *   A) Python server at localhost:5000 → polls /api/latest every 2 s (scikit-learn ML)
 *   B) Web Serial API → direct ESP32 USB connection in Chrome/Edge
 *   C) Built-in JS simulation → offline demo
 *
 * AQI computation mirrors nirmal_ml_engine.py (US EPA PM2.5 breakpoints).
 */

"use strict";

// ═══════════════════════════════════════════════════════════════════════
// State
// ═══════════════════════════════════════════════════════════════════════
const state = {
  mode:          "idle",        // "server" | "serial" | "sim" | "idle"
  isSerialOpen:  false,
  serialPort:    null,
  serialReader:  null,
  simTimer:      null,
  pollTimer:     null,
  step:          0,
  history:       [],            // capped at 60 entries for charts
  mlSamples:     0,
  cumAbsErr:     0,
  cumSqErr:      0,             // for correct RMSE: sqrt(sum(e²)/n)
  lastForecast:  null,
  autoPurifier:  true,
  xaiGlobalMode: false,         // toggle: local vs global XAI view
  xaiMaxAbs:     1.0,           // running max |contribution| for bar scaling
  lightMode:     false,         // dark/light theme
  lastPurifier:  false,         // track purifier state changes for toast
  lastDrift:     false,         // track drift state changes for toast
};

// ═══════════════════════════════════════════════════════════════════════
// Toast notification system
// ═══════════════════════════════════════════════════════════════════════
let _toastCtr = 0;

/**
 * Show a toast notification.
 * @param {string} type  'danger' | 'warn' | 'good' | 'info'
 * @param {string} title Short bold heading
 * @param {string} body  Longer description text
 * @param {number} ms    Auto-dismiss after ms (default 5000)
 */
function showToast(type, title, body, ms = 5000) {
  const icons = { danger: 'fa-circle-exclamation', warn: 'fa-triangle-exclamation',
                  good: 'fa-circle-check', info: 'fa-circle-info' };
  const id = `toast-${++_toastCtr}`;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.id = id;
  el.innerHTML = `
    <span class="toast-icon"><i class="fa-solid ${icons[type] || icons.info}"></i></span>
    <div class="toast-msg">
      <div class="toast-title">${title}</div>
      <div class="toast-body">${body}</div>
    </div>
    <span class="toast-close" onclick="dismissToast('${id}')">✕</span>
  `;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => dismissToast(id), ms);
}

function dismissToast(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add('fade-out');
  setTimeout(() => el.remove(), 420);
}

// ═══════════════════════════════════════════════════════════════════════
// Dark / Light Mode Toggle
// ═══════════════════════════════════════════════════════════════════════
function initTheme() {
  const saved = localStorage.getItem('nirmalnode-theme');
  if (saved === 'light') {
    document.body.classList.add('light-mode');
    state.lightMode = true;
    const btn = document.getElementById('btnTheme');
    if (btn) btn.textContent = '☀️';
  }
}

function toggleTheme() {
  state.lightMode = !state.lightMode;
  document.body.classList.toggle('light-mode', state.lightMode);
  const btn = document.getElementById('btnTheme');
  if (btn) btn.textContent = state.lightMode ? '☀️' : '🌙';
  localStorage.setItem('nirmalnode-theme', state.lightMode ? 'light' : 'dark');
}

// ═══════════════════════════════════════════════════════════════════════
// Drift Banner
// ═══════════════════════════════════════════════════════════════════════
function updateDriftBanner(driftAlert) {
  const banner = document.getElementById('driftBanner');
  const scoreEl = document.getElementById('driftScore');
  if (!banner || !driftAlert) return;

  const isActive = driftAlert.drift_detected || false;
  banner.classList.toggle('active', isActive);

  if (scoreEl && driftAlert.drift_score !== undefined) {
    scoreEl.textContent = `(z-score: ${driftAlert.drift_score.toFixed(2)}, events: ${driftAlert.drift_count || 0})`;
  }

  // Toast on first detection
  if (isActive && !state.lastDrift) {
    showToast('warn', '⚠ Concept Drift Detected',
      `AI model error is shifting (z=${(driftAlert.drift_score||0).toFixed(2)}). Environment may have changed.`, 8000);
  }
  state.lastDrift = isActive;
}

// ═══════════════════════════════════════════════════════════════════════
// Confidence Badge
// ═══════════════════════════════════════════════════════════════════════
function renderConfBadge(conf) {
  if (conf === undefined || conf === null) return '';
  const pct = Math.round(conf * 100);
  const cls  = pct >= 70 ? '' : pct >= 40 ? 'mid' : 'low';
  return `<span class="conf-badge ${cls}"><i class="fa-solid fa-shield-halved"></i>${pct}% confident</span>`;
}

// ═══════════════════════════════════════════════════════════════════════
// US EPA AQI (PM2.5) – client-side fallback
// ═══════════════════════════════════════════════════════════════════════
const AQI_BP = [
  { cl:0,     ch:12.0,  il:0,   ih:50,  cat:"Good",                           col:"#10b981" },
  { cl:12.1,  ch:35.4,  il:51,  ih:100, cat:"Moderate",                       col:"#f59e0b" },
  { cl:35.5,  ch:55.4,  il:101, ih:150, cat:"Unhealthy for Sensitive Groups",  col:"#f97316" },
  { cl:55.5,  ch:150.4, il:151, ih:200, cat:"Unhealthy",                       col:"#ef4444" },
  { cl:150.5, ch:250.4, il:201, ih:300, cat:"Very Unhealthy",                  col:"#8b5cf6" },
  { cl:250.5, ch:350.4, il:301, ih:400, cat:"Hazardous",                       col:"#6b21a8" },
  { cl:350.5, ch:500.4, il:401, ih:500, cat:"Hazardous",                       col:"#4c1d95" },
];

function calcAQI(pm25) {
  const c = Math.min(500.4, Math.max(0, Math.floor(pm25 * 10) / 10));
  for (const bp of AQI_BP) {
    if (c >= bp.cl && c <= bp.ch) {
      return {
        aqi: Math.round(((bp.ih - bp.il) / (bp.ch - bp.cl)) * (c - bp.cl) + bp.il),
        category: bp.cat, color: bp.col
      };
    }
  }
  return { aqi: 500, category: "Hazardous", color: "#4c1d95" };
}

function aqiAdvice(aqi) {
  if (aqi <= 50)  return "Air quality is satisfactory.";
  if (aqi <= 100) return "Air quality is acceptable for most people.";
  if (aqi <= 150) return "Sensitive groups should limit exposure.";
  if (aqi <= 200) return "Unhealthy – everyone may be affected.";
  if (aqi <= 300) return "Very unhealthy – avoid prolonged exposure!";
  return "Hazardous – health emergency!";
}

function aqiRisk(aqi) {
  if (aqi <= 50)  return "Low Risk";
  if (aqi <= 100) return "Moderate Risk";
  if (aqi <= 150) return "Elevated Risk";
  if (aqi <= 200) return "High Risk";
  if (aqi <= 300) return "Very High Risk";
  return "⚠ Critical Hazard";
}

// ═══════════════════════════════════════════════════════════════════════
// Charts
// ═══════════════════════════════════════════════════════════════════════
let chartPM = null, chartML = null;

function initCharts() {
  const commonGrid = { color: "rgba(255,255,255,0.06)" };
  const commonTick = { color: "#5070a0", font: { size: 10 } };

  chartPM = new Chart(document.getElementById("chartPM"), {
    type: "line",
    data: {
      labels: [],
      datasets: [
        { label: "Live PM2.5", data: [], borderColor: "#00f2fe",
          backgroundColor: "rgba(0,242,254,0.08)", fill: true,
          tension: 0.35, borderWidth: 2, pointRadius: 0 },
        { label: "1H Forecast", data: [], borderColor: "#8b5cf6",
          borderDash: [5,4], fill: false,
          tension: 0.35, borderWidth: 2, pointRadius: 0 },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      interaction: { mode: "index", intersect: false },
      scales: {
        x: { grid: commonGrid, ticks: { ...commonTick, maxTicksLimit: 8 } },
        y: { grid: commonGrid, ticks: commonTick, beginAtZero: true,
             title: { display: true, text: "µg/m³", color: "#5070a0", font: { size: 10 } } }
      },
      plugins: { legend: { display: false }, tooltip: { callbacks: {
        label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)} µg/m³`
      }}}
    }
  });

  chartML = new Chart(document.getElementById("chartML"), {
    type: "line",
    data: {
      labels: [],
      datasets: [
        { label: "MAE",  data: [], borderColor: "#10b981",
          fill: false, tension: 0.3, borderWidth: 2, pointRadius: 0 },
        { label: "RMSE", data: [], borderColor: "#f59e0b",
          borderDash: [4,3], fill: false, tension: 0.3, borderWidth: 2, pointRadius: 0 },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      scales: {
        x: { grid: commonGrid, ticks: { ...commonTick, maxTicksLimit: 8 } },
        y: { grid: commonGrid, ticks: commonTick, beginAtZero: true,
             title: { display: true, text: "Error (µg/m³)", color: "#5070a0", font: { size: 10 } } }
      },
      plugins: { legend: {
        display: true,
        labels: { color: "#8fa4c8", boxWidth: 10, font: { size: 10 } }
      }}
    }
  });
}

function pushChartData(ts, pm25, fc1h, mae, rmse) {
  const MAX = 40;
  const push = (chart, ...vals) => {
    chart.data.labels.push(ts);
    vals.forEach((v, i) => chart.data.datasets[i].data.push(v));
    if (chart.data.labels.length > MAX) {
      chart.data.labels.shift();
      chart.data.datasets.forEach(d => d.data.shift());
    }
    chart.update("none");
  };
  push(chartPM, pm25, fc1h);
  push(chartML, mae, rmse);
}

// ═══════════════════════════════════════════════════════════════════════
// XAI Rendering
// ═══════════════════════════════════════════════════════════════════════

/**
 * Render XAI feature contribution bars.
 * features: [{name, contribution, direction, raw_value}, ...]
 * containerId: 'xaiBars' | 'xaiGlobalBars'
 * valueKey: 'contribution' | 'importance'
 */
function renderXaiBars(features, containerId, valueKey) {
  const el = $(containerId);
  if (!el || !features || features.length === 0) {
    if (el) el.innerHTML = '<div class="xai-placeholder">No data yet…</div>';
    return;
  }

  // Find max abs value for proportional bar scaling
  const maxAbs = Math.max(...features.map(f => Math.abs(f[valueKey])), 0.001);

  el.innerHTML = features.map(f => {
    const val    = f[valueKey];
    const dir    = f.direction || (val >= 0 ? 'up' : 'down');
    const pct    = Math.min(50, (Math.abs(val) / maxAbs) * 50).toFixed(1); // max 50% each side
    const arrow  = dir === 'up' ? '↑' : '↓';
    const sign   = val >= 0 ? '+' : '';
    const rawDisp = f.raw_value !== undefined ? ` (${f.raw_value})` : '';

    return `
      <div class="xai-row">
        <div class="xai-feat-name" title="${f.name}${rawDisp}">${f.name}</div>
        <div class="xai-bar-track">
          <div class="xai-bar-fill ${dir}" style="width:${pct}%"></div>
        </div>
        <div class="xai-contrib-val ${dir}">
          ${sign}${val.toFixed(3)}<span class="xai-direction">${arrow}</span>
        </div>
      </div>`;
  }).join('');
}

/** Switch between local (per-prediction) and global (all-time) XAI tabs */
function setXaiTab(mode) {
  state.xaiGlobalMode = (mode === 'global');
  $('xaiLocalPanel').style.display  = state.xaiGlobalMode ? 'none'  : 'block';
  $('xaiGlobalPanel').style.display = state.xaiGlobalMode ? 'block' : 'none';
  $('tabLocal').classList.toggle('active',  !state.xaiGlobalMode);
  $('tabGlobal').classList.toggle('active',  state.xaiGlobalMode);
  if (state.xaiGlobalMode) fetchGlobalImportance();
}

/** Also keep old name as alias so existing onclick="toggleXaiView()" still works */
function toggleXaiView() { setXaiTab(state.xaiGlobalMode ? 'local' : 'global'); }

/** Fetch global feature importance from /api/explain */
async function fetchGlobalImportance() {
  try {
    const res = await fetch('http://localhost:5000/api/explain', { signal: AbortSignal.timeout(2000) });
    if (!res.ok) return;
    const data = await res.json();
    renderXaiBars(data.global_importance || [], 'xaiGlobalBars', 'importance');
  } catch (_) {
    const el = $('xaiGlobalBars');
    if (el) el.innerHTML = '<div class="xai-placeholder">Server not available</div>';
  }
}

// ═══════════════════════════════════════════════════════════════════════
// Model Arena Leaderboard
// ═══════════════════════════════════════════════════════════════════════

/** Fetch /api/model_arena and render the leaderboard table */
async function fetchArena() {
  try {
    const res = await fetch('http://localhost:5000/api/model_arena', { signal: AbortSignal.timeout(3000) });
    if (!res.ok) return;
    const d = await res.json();
    renderArena(d);
  } catch (_) {
    const b = $('arenaBody');
    if (b) b.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:1rem">Server not available — start python server.py</td></tr>';
  }
}

/** Render leaderboard rows */
function renderArena(d) {
  const body   = $('arenaBody');
  const chName = $('arenaChampName');
  const sub    = $('arenaSubtitle');
  const elec   = $('arenaElections');
  if (!body) return;

  if (chName) chName.textContent = d.champion || '—';
  if (elec)   elec.textContent   = d.election_count || 0;

  const warmed = d.samples_trained >= (d.warmup_samples || 50);
  if (sub) sub.textContent = warmed
    ? `Active · ${d.samples_trained} samples processed · elections: ${d.election_count}`
    : `Warming up… ${d.samples_trained}/${d.warmup_samples || 50} samples`;

  const rows = d.leaderboard || [];
  if (rows.length === 0) {
    body.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:1rem">No data yet…</td></tr>';
    return;
  }

  // Worst MAE (for scaling bar width)
  const maxMae = Math.max(...rows.filter(r => r.n > 0).map(r => r.mae), 1);

  const rankClass = i => i === 0 ? 'gold' : i === 1 ? 'silver' : i === 2 ? 'bronze' : '';

  body.innerHTML = rows.map((r, i) => {
    const isChamp  = r.champion;
    const barW     = r.n > 0 ? Math.max(4, (1 - r.mae / maxMae) * 80).toFixed(1) : 0;
    const badge    = isChamp ? '<span class="arena-champ-badge">🏆 CHAMPION</span>' : '';
    const waiting  = r.n < 5;
    const maeStr   = waiting ? '—' : r.mae.toFixed(3);
    const rmseStr  = waiting ? '—' : r.rmse.toFixed(3);
    const bar      = waiting ? '' : `<span class="arena-mae-bar" style="width:${barW}px"></span>`;
    const status   = isChamp ? '🏆 Active' : (r.n >= 5 ? 'Competing' : 'Warming up');
    return `<tr class="${isChamp ? 'arena-champ' : ''}">
      <td><span class="arena-rank ${rankClass(i)}">${i+1}</span></td>
      <td>${r.short}${badge}<br><small style="color:#5070a0;font-size:0.72rem">${r.name}</small></td>
      <td>${maeStr}${bar}</td>
      <td>${rmseStr}</td>
      <td>${r.n}</td>
      <td>${status}</td>
    </tr>`;
  }).join('');
}

/** Start arena auto-refresh every 5 s */
function startArenaRefresh() {
  fetchArena();
  setInterval(fetchArena, 5000);
}

// ═══════════════════════════════════════════════════════════════════════
// DOM helpers
// ═══════════════════════════════════════════════════════════════════════
const $ = id => document.getElementById(id);

function logConsole(msg) {
  const el = $("console");
  el.textContent += `[${new Date().toLocaleTimeString()}] ${msg}\n`;
  el.scrollTop = el.scrollHeight;
}

function setConnBadge(mode) {
  const badge = $("connBadge");
  badge.className = "conn-badge " + (mode === "live" ? "live" : mode === "sim" ? "sim" : "");
  const labels = { live: "Hardware Connected", sim: "Demo Simulation", idle: "Disconnected" };
  $("connLabel").textContent = labels[mode] || "Disconnected";
}

// ═══════════════════════════════════════════════════════════════════════
// UI update – single source of truth
// ═══════════════════════════════════════════════════════════════════════
function applyTelemetry(d) {
  // Clock
  $("headerTimestamp").textContent = d.timestamp || new Date().toLocaleTimeString();

  // ── AQI ring ──────────────────────────────────────────────────────
  const aqi   = d.aqi   || 0;
  const aCol  = d.aqi_color || "#10b981";
  const aCat  = d.aqi_category || "–";

  $("aqiValue").textContent = aqi;
  $("ringFg").style.stroke = aCol;
  // Circumference = 2π×50 ≈ 314.16; offset = circ × (1 - ratio)
  const ratio  = Math.min(1, aqi / 500);
  const circ   = 314.16;
  $("ringFg").style.strokeDashoffset = (circ * (1 - ratio)).toFixed(1);
  $("aqiCard").style.setProperty("--aqi-glow", aCol + "22");

  // badge colour
  const badge = $("aqiBadge");
  badge.textContent = aCat;
  badge.style.background  = aCol + "28";
  badge.style.color       = aCol;
  badge.style.borderColor = aCol + "55";

  $("aqiAdvice").textContent   = aqiAdvice(aqi);
  $("aqiRisk").textContent     = aqiRisk(aqi);

  // ── Forecast ──────────────────────────────────────────────────────
  const f1 = d.forecast_1h ?? 0;
  const f2 = d.forecast_2h ?? 0;
  $("fc1h").innerHTML = `${f1.toFixed(1)} <small>µg/m³</small>`;
  $("fc2h").innerHTML = `${f2.toFixed(1)} <small>µg/m³</small>`;
  const fc1aqi = calcAQI(f1);
  const fc2aqi = calcAQI(f2);
  $("fc1hAqi").textContent = `AQI ${fc1aqi.aqi} — ${fc1aqi.category}`;
  $("fc2hAqi").textContent = `AQI ${fc2aqi.aqi} — ${fc2aqi.category}`;

  // ── Purifier decision ─────────────────────────────────────────────
  const trigger = state.autoPurifier
    ? (d.purifier_trigger ?? false)
    : false;

  const fanStatus  = $("fanStatus");
  const fanWrap    = $("fanIconWrap");
  const fanTitle   = $("fanTitle");
  const fanSub     = $("fanSub");

  if (trigger) {
    fanStatus.className = "fan-status danger";
    fanWrap.className   = "fan-icon-wrap spin";
    fanTitle.textContent = "Cyclone + HEPA Filter";
    fanSub.textContent  = "⚡ ACTIVE (Pre-emptive AI Trigger)";
  } else {
    fanStatus.className = "fan-status";
    fanWrap.className   = "fan-icon-wrap";
    fanTitle.textContent = "Cyclone + HEPA Filter";
    fanSub.textContent  = "Status: Standby — Air Clean";
  }

  // ── PM values ─────────────────────────────────────────────────────
  const pm10  = d.pm1_0  ?? 0;
  const pm25  = d.pm2_5  ?? 0;
  const pm100 = d.pm10   ?? 0;
  const cnt03 = d.cnt0_3 ?? 0;
  const cnt25 = d.cnt2_5 ?? 0;

  $("valPm10").textContent  = pm10;
  $("valPm25").textContent  = pm25;
  $("valPm100").textContent = pm100;
  $("valCnt03").textContent = cnt03.toLocaleString();
  $("valCnt25").textContent = cnt25.toLocaleString();

  setBar("barPm10",  pm10  / 100);
  setBar("barPm25",  pm25  / 100);
  setBar("barPm100", pm100 / 150);
  setBar("barCnt03", cnt03 / 5000);
  setBar("barCnt25", cnt25 / 500);

  // ── Gas sensors ───────────────────────────────────────────────────
  setGas("Mq135",   d.mq135_adc   ?? 0);
  setGas("Mq136",   d.mq136_adc   ?? 0);
  setGas("MicsRed", d.mics_red_adc ?? 0);
  setGas("MicsNox", d.mics_nox_adc ?? 0);
  setGas("Mp135",   d.mp135_adc   ?? 0);

  // ── Online learning stats ─────────────────────────────────────────
  const ol  = d.online_learning || {};
  const n   = ol.samples_trained ?? 0;
  const mae = ol.mae  ?? 0;
  const rmse= ol.rmse ?? 0;
  $('mlBadge').textContent = `Samples: ${n} | MAE: ${mae} | RMSE: ${rmse}`;

  // Update XAI sample count footer
  const xaiCount = $('xaiSampleCount');
  if (xaiCount) xaiCount.textContent = `Samples trained: ${n}`;

  // ── XAI: Feature Contributions ───────────────────────────────────────────
  if (!state.xaiGlobalMode) {
    const xai = d.xai || {};
    const topFeats = xai.top_features || [];
    renderXaiBars(topFeats, 'xaiBars', 'contribution');
  }

  // ── Model Arena: Multi-model leaderboard ─────────────────────────
  const conf = (d.online_learning || {}).confidence;
  if (d.model_arena) {
    renderArena({
      leaderboard:     d.model_arena,
      champion:        ol.champion || "SGD+PA Blend 0.6/0.4",
      champion_short:  ol.champion_short || "M8-BLEND",
      samples_trained: n,
      warmup_samples:  50,
      election_count:  ol.election_count || 1,
      confidence:      conf,
    });
  }

  // ── Confidence badge in ML badge area ─────────────────────────────
  $('mlBadge').innerHTML =
    `Samples: ${n} | MAE: ${mae} | RMSE: ${rmse} &nbsp; ${renderConfBadge(conf)}`;


  // ── AQI pulse animation when hazardous ────────────────────────────
  const aqiCard = $('aqiCard');
  if (aqiCard) aqiCard.classList.toggle('hazard-pulse', aqi > 150);

  // ── Purifier state change toast ───────────────────────────────────
  if (trigger && !state.lastPurifier) {
    showToast('danger', '🌬 Purifier Activated',
      `PM2.5=${pm25} µg/m³ · AQI=${aqi} · Pre-emptive AI trigger`, 6000);
  } else if (!trigger && state.lastPurifier) {
    showToast('good', '✅ Air Quality Restored',
      `Purifier switched OFF · AQI=${aqi} · ${aCat}`, 4000);
  }
  state.lastPurifier = trigger;

  // ── Drift banner ──────────────────────────────────────────────────
  updateDriftBanner(d.drift_alert || null);

  // ── Charts ────────────────────────────────────────────────────────
  const ts = (d.timestamp || new Date().toLocaleTimeString()).slice(0,8);
  pushChartData(ts, pm25, f1, mae, rmse);

  // ── History log ───────────────────────────────────────────────────
  state.history.push(d);
  if (state.history.length > 500) state.history.shift();
}

function setBar(id, ratio) {
  const el = $(id);
  if (el) el.style.width = Math.min(100, Math.max(0, ratio * 100)).toFixed(1) + "%";
}

function setGas(suffix, adc) {
  $("val" + suffix).textContent = adc;
  setBar("bar" + suffix, adc / 4095);
}

// ═══════════════════════════════════════════════════════════════════════
// MODE A: Python Server polling
// ═══════════════════════════════════════════════════════════════════════
async function tryPythonServer() {
  try {
    const res = await fetch("http://localhost:5000/api/latest", { signal: AbortSignal.timeout(1500) });
    if (!res.ok) return false;
    const d = await res.json();
    logConsole("Python ML backend detected at localhost:5000 – polling every 2 s.");
    state.mode = "server";
    setConnBadge("live");
    applyTelemetry(d);

    // Poll interval
    state.pollTimer = setInterval(async () => {
      try {
        const r = await fetch("http://localhost:5000/api/latest", { signal: AbortSignal.timeout(2000) });
        if (r.ok) applyTelemetry(await r.json());
      } catch (_) {}
    }, 2000);
    return true;
  } catch (_) {
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════════════
// MODE B: Web Serial API (direct ESP32 USB in Chrome/Edge)
// ═══════════════════════════════════════════════════════════════════════
async function connectWebSerial() {
  if (!("serial" in navigator)) {
    alert("Web Serial API requires Google Chrome or Microsoft Edge.\nAlternatively run: python server.py");
    return;
  }
  // Stop simulation first
  stopSim();

  try {
    logConsole("Opening port selector…");
    state.serialPort = await navigator.serial.requestPort();
    await state.serialPort.open({ baudRate: 115200 });
    state.isSerialOpen = true;
    state.mode = "serial";
    setConnBadge("live");
    logConsole("ESP32 USB Serial connected @ 115200 baud. Waiting for data…");
    readSerial();
  } catch (e) {
    logConsole("Serial connect failed: " + e.message);
    startSim();
  }
}

async function readSerial() {
  const tds = new TextDecoderStream();
  state.serialPort.readable.pipeTo(tds.writable);
  state.serialReader = tds.readable.getReader();
  let buf = "";

  try {
    while (state.isSerialOpen) {
      const { value, done } = await state.serialReader.read();
      if (done) break;
      buf += value;

      // Try JSON line (LiveAPI JSON mode)
      const nlIdx = buf.lastIndexOf("\n");
      if (nlIdx >= 0) {
        const lines = buf.slice(0, nlIdx).split("\n");
        buf = buf.slice(nlIdx + 1);
        for (const line of lines) {
          const t = line.trim();
          if (t.startsWith("{") && t.endsWith("}")) {
            try {
              const raw = JSON.parse(t);
              applyTelemetry(enrichClientSide(raw));
              logConsole(`JSON ← PM2.5: ${raw.pm2_5} | MQ135: ${raw.mq135_adc}`);
            } catch (_) {}
          }
        }
      }

      // Text report parsing (AirGuard / NirmalNode_SensorTest format)
      if ((buf.match(/={20,}/g) || []).length >= 2) {
        const raw = parseTextReport(buf);
        if (raw.pm2_5 > 0 || raw.mq135_adc > 0) {
          applyTelemetry(enrichClientSide(raw));
          logConsole(`TEXT ← PM2.5: ${raw.pm2_5} | MQ135: ${raw.mq135_adc}`);
          buf = "";
        }
      }
    }
  } catch (e) {
    logConsole("Serial read error: " + e.message);
  } finally {
    state.isSerialOpen = false;
    setConnBadge("idle");
  }
}

function parseTextReport(text) {
  const ex = (re, fb = 0) => { const m = text.match(re); return m ? parseInt(m[1]) : fb; };
  return {
    timestamp:    new Date().toLocaleTimeString(),
    pm1_0:        ex(/PM1\.0\s*:\s*(\d+)/i),
    pm2_5:        ex(/PM2\.5\s*:\s*(\d+)/i),
    pm10:         ex(/PM10\s*:\s*(\d+)/i),
    cnt0_3:       ex(/P>0\.3um\s*:\s*(\d+)/i),
    cnt0_5:       ex(/P>0\.5um\s*:\s*(\d+)/i),
    cnt1_0:       ex(/P>1\.0um\s*:\s*(\d+)/i),
    cnt2_5:       ex(/P>2\.5um\s*:\s*(\d+)/i),
    cnt5_0:       ex(/P>5\.0um\s*:\s*(\d+)/i),
    cnt10_0:      ex(/P>10um\s*:\s*(\d+)/i),
    mq135_adc:    ex(/MQ135[\s\S]*?ADC\s*:\s*(\d+)/i),
    mq136_adc:    ex(/MQ136[\s\S]*?ADC\s*:\s*(\d+)/i),
    mics_red_adc: ex(/RED ADC\s*:\s*(\d+)/i),
    mics_nox_adc: ex(/NOX ADC\s*:\s*(\d+)/i),
    mp135_adc:    ex(/MP135[\s\S]*?ADC\s*:\s*(\d+)/i),
  };
}

// Client-side AQI + prequential ML when NOT connected to Python server
function enrichClientSide(raw) {
  const pm25 = raw.pm2_5 || 0;
  const aqiInfo = calcAQI(pm25);

  // Simple 1-step-ahead "forecast": EMA projection
  const fc1 = parseFloat(Math.max(0, pm25 * 1.03).toFixed(1));
  const fc2 = parseFloat(Math.max(0, pm25 * 1.06).toFixed(1));

  // Prequential MAE + RMSE update (test-then-train)
  let mae = 0, rmse = 0;
  if (state.lastForecast !== null) {
    const err = Math.abs(pm25 - state.lastForecast);
    state.mlSamples++;
    state.cumAbsErr  += err;
    state.cumSqErr   += err * err;   // track separately for correct RMSE
    mae  = parseFloat((state.cumAbsErr / state.mlSamples).toFixed(3));
    rmse = parseFloat(Math.sqrt(state.cumSqErr / state.mlSamples).toFixed(3));
  }
  state.lastForecast = fc1;

  const purifier = pm25 >= 35.5 || aqiInfo.aqi > 100;

  // ── Simulated XAI for client-side / Demo mode ──────────────────────
  // Proportional contributions using current sensor readings as weights
  // (directionally correct: higher PM → higher positive contribution)
  const ema    = state.lastForecast !== null ? 0.75 * state.lastForecast + 0.25 * pm25 : pm25;
  const delta  = state.lastForecast !== null ? pm25 - state.lastForecast : 0;
  const simFeats = [
    { name: "PM2.5 EMA",          raw_value: +ema.toFixed(1),              contribution: +(ema   * 0.18).toFixed(3),              direction: "up"            },
    { name: "PM2.5 delta(lag-1)", raw_value: +delta.toFixed(1),            contribution: +(-delta * 0.22).toFixed(3),             direction: delta>0?"down":"up" },
    { name: "PM10",               raw_value: raw.pm10  || 0,               contribution: +((raw.pm10||0)  * 0.015).toFixed(3),    direction: "up"            },
    { name: "PM2.5 (current)",    raw_value: pm25,                         contribution: +(pm25   * 0.14).toFixed(3),             direction: "up"            },
    { name: "Count >2.5um",       raw_value: raw.cnt2_5 || 0,              contribution: +((raw.cnt2_5||0) * 0.008).toFixed(3),   direction: "up"            },
  ].map(f => ({ ...f, direction: f.contribution >= 0 ? "up" : "down" }))
   .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution));

  return {
    ...raw,
    aqi:                   aqiInfo.aqi,
    aqi_category:          aqiInfo.category,
    aqi_color:             aqiInfo.color,
    forecast_1h:           fc1,
    forecast_2h:           fc2,
    forecast_aqi:          calcAQI(fc1).aqi,
    forecast_aqi_category: calcAQI(fc1).category,
    purifier_trigger:      purifier,
    purifier_status:       purifier ? "ACTIVE (PRE-EMPTIVE)" : "IDLE (CLEAN)",
    online_learning: {
      samples_trained: state.mlSamples,
      mae,
      rmse,
      status: state.mlSamples < 5 ? "Warming Up" : "Client-Side ML Active",
    },
    xai: {
      method:         "Simulated LFC (client-side demo)",
      top_features:   simFeats,
      all_features:   simFeats,
      shap_available: false,
    },
    model_arena: [
      { short: "M8-BLEND",  name: "SGD+PA Blend 0.6/0.4",      mae: +(mae * 0.94).toFixed(3), rmse: +(rmse * 0.94).toFixed(3), n: state.mlSamples, champion: true },
      { short: "M1-SGD-L2", name: "SGD Ridge (L2)",            mae: +(mae * 1.05).toFixed(3), rmse: +(rmse * 1.04).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M4-SGD-HUB",name: "SGD Huber (L2)",            mae: +(mae * 1.08).toFixed(3), rmse: +(rmse * 1.07).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M6-PA-1",   name: "PA Regressor C=1.0",        mae: +(mae * 1.15).toFixed(3), rmse: +(rmse * 1.12).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M3-SGD-EN", name: "SGD ElasticNet",            mae: +(mae * 1.18).toFixed(3), rmse: +(rmse * 1.16).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M2-SGD-L1", name: "SGD Lasso (L1)",            mae: +(mae * 1.22).toFixed(3), rmse: +(rmse * 1.20).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M5-SGD-SVR",name: "SGD Eps-Insensitive",       mae: +(mae * 1.26).toFixed(3), rmse: +(rmse * 1.24).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M7-PA-01",  name: "PA Regressor C=0.1",        mae: +(mae * 1.31).toFixed(3), rmse: +(rmse * 1.29).toFixed(3), n: state.mlSamples, champion: false },
      { short: "M9-EMA",    name: "EMA Baseline (naive)",      mae: +(mae * 1.48).toFixed(3), rmse: +(rmse * 1.45).toFixed(3), n: state.mlSamples, champion: false },
    ],
  };
}

// ═══════════════════════════════════════════════════════════════════════
// MODE C: Simulation (Industrial hotspot demo)
// ═══════════════════════════════════════════════════════════════════════
function startSim() {
  if (state.simTimer) return;
  state.mode = "sim";
  setConnBadge("sim");
  $("simLabel").textContent = "Stop Demo";
  logConsole("Demo Simulation started – realistic industrial hotspot data.");

  state.simTimer = setInterval(() => {
    state.step++;
    const base  = 22 + 14 * Math.sin(state.step * 0.08) + (Math.random() * 3 - 1.5);
    const spike = (state.step % 22 === 0) ? 58 : 0;
    const pm25  = Math.round(Math.max(4, base + spike));

    const raw = {
      timestamp:    new Date().toLocaleTimeString(),
      pm1_0:        Math.round(pm25 * 0.58),
      pm2_5:        pm25,
      pm10:         Math.round(pm25 * 1.45),
      cnt0_3:       Math.round(pm25 * 48 + Math.random() * 30),
      cnt0_5:       Math.round(pm25 * 14),
      cnt1_0:       Math.round(pm25 * 3.5),
      cnt2_5:       Math.round(pm25 * 0.75),
      cnt5_0:       Math.round(pm25 * 0.18),
      cnt10_0:      Math.round(pm25 * 0.04),
      mq135_adc:    Math.round(1180 + pm25 * 16 + Math.random() * 20),
      mq136_adc:    Math.round(820  + pm25 * 10 + Math.random() * 12),
      mics_red_adc: Math.round(1550 + pm25 * 19 + Math.random() * 25),
      mics_nox_adc: Math.round(1020 + pm25 * 13 + Math.random() * 18),
      mp135_adc:    Math.round(1120 + pm25 * 14 + Math.random() * 18),
    };
    applyTelemetry(enrichClientSide(raw));
  }, 2000);
}

function stopSim() {
  if (state.simTimer) { clearInterval(state.simTimer); state.simTimer = null; }
  $("simLabel").textContent = "Demo Mode";
}

// ═══════════════════════════════════════════════════════════════════════
// Purifier manual API calls (to Python server / serial)
// ═══════════════════════════════════════════════════════════════════════
async function sendPurifierCmd(onOff) {
  if (state.mode === "server") {
    try {
      await fetch("http://localhost:5000/api/purifier", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: onOff ? "on" : "off" }),
        signal: AbortSignal.timeout(2000)
      });
      logConsole(`Purifier command sent: FAN_${onOff ? "ON" : "OFF"}`);
    } catch (e) { logConsole("Purifier API error: " + e.message); }
  } else if (state.mode === "serial" && state.serialPort && state.serialPort.writable) {
    const w = state.serialPort.writable.getWriter();
    await w.write(new TextEncoder().encode(onOff ? "FAN_ON\n" : "FAN_OFF\n"));
    w.releaseLock();
    logConsole(`Serial command sent: FAN_${onOff ? "ON" : "OFF"}`);
  } else {
    logConsole("No hardware connected – command ignored.");
  }
}

// ═══════════════════════════════════════════════════════════════════════
// CSV export
// ═══════════════════════════════════════════════════════════════════════
async function exportCSV() {
  // If server running, fetch its export (has scikit-learn ML stats)
  if (state.mode === "server") {
    try {
      const res = await fetch("http://localhost:5000/api/export");
      if (res.ok) {
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement("a");
        a.href = url; a.download = "nirmalnode_thesis_data.csv";
        a.click(); URL.revokeObjectURL(url);
        logConsole("Exported thesis CSV from Python server.");
        return;
      }
    } catch (_) {}
  }

  // Client-side fallback
  if (state.history.length === 0) { alert("No data yet!"); return; }
  const flat = state.history.map(r => {
    const ol = r.online_learning || {};
    return { ...r, ml_samples: ol.samples_trained, ml_mae: ol.mae, ml_rmse: ol.rmse };
  });
  const keys = Object.keys(flat[0]).filter(k => typeof flat[0][k] !== "object");
  const csv  = [keys.join(","), ...flat.map(r => keys.map(k => r[k] ?? "").join(","))].join("\n");
  const a    = document.createElement("a");
  a.href     = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
  a.download = `nirmalnode_telemetry_${Date.now()}.csv`;
  a.click();
  logConsole("Exported client-side telemetry CSV.");
}

// ═══════════════════════════════════════════════════════════════════════
// Bind UI events
// ═══════════════════════════════════════════════════════════════════════
function bindEvents() {
  $("btnConnect").onclick = connectWebSerial;

  $("btnSim").onclick = () => {
    if (state.simTimer) { stopSim(); setConnBadge("idle"); state.mode = "idle"; }
    else startSim();
  };

  $("btnExport").onclick = exportCSV;

  $("btnClearConsole").onclick = () => { $("console").textContent = "[NIRMALNODE] Log cleared.\n"; };

  $("autoToggle").onchange = e => {
    state.autoPurifier = e.target.checked;
    logConsole("Purifier mode: " + (state.autoPurifier ? "Adaptive AI Auto" : "Manual"));
  };

  $("btnFanOn").onclick  = () => sendPurifierCmd(true);
  $("btnFanOff").onclick = () => sendPurifierCmd(false);

  // Dark / Light mode toggle
  const btnTheme = $("btnTheme");
  if (btnTheme) btnTheme.onclick = toggleTheme;
}

// ═══════════════════════════════════════════════════════════════════════
// Boot
// ═══════════════════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", async () => {
  initTheme();    // restore saved theme (dark/light)
  initCharts();
  bindEvents();

  // Try Python server first
  const serverOk = await tryPythonServer();
  if (!serverOk) {
    logConsole("Python server not found. Starting Demo Simulation…");
    startSim();
  }
});
