/*
  ===========================================================================
  NirmalNode – WiFi-Enabled Live Air Quality Node
  ---------------------------------------------------------------------------
  BOARD            : ESP32 DevKit V1 (ESP-WROOM-32, 30-pin)
  CORE             : ESP32 Arduino Core 3.x

  ⚡ QUICK SETUP – সব পরিবর্তন এই দুটো লাইনেই:
     #define WIFI_SSID   "আপনার WiFi নাম"
     #define WIFI_PASS   "আপনার WiFi পাসওয়ার্ড"
     #define SERVER_IP   "আপনার পিসির IP" (যে পিসিতে server.py চলছে)

  HOW IT WORKS:
    1. ESP32 চালু হলে WiFi তে connect করে
    2. প্রতি 2 সেকেন্ডে সব sensor পড়ে
    3. JSON হিসেবে server.py তে HTTP POST করে
       → server.py সেই data নিয়ে ML model চালায়
       → Dashboard এ live দেখা যায়
    4. Serial Monitor এও সব print করে (debug এর জন্য)

  SENSORS:
    PMS5003    (UART2, GPIO16)  - PM1.0, PM2.5, PM10 + Particle Counts
    MQ135      (GPIO32)         - CO2 / NH3 (calibrated estimate)
    MQ136      (GPIO33)         - H2S / Sulphur
    MiCS-4514 RED (GPIO34)     - CO (Carbon Monoxide)
    MiCS-4514 NOX (GPIO35)     - NO2 (Nitrogen Dioxide)
    MP135      (GPIO36)         - VOC Index

  RELAY CONTROL:
    GPIO18  – Cyclone+HEPA Fan relay (server থেকে FAN_ON/FAN_OFF command এ চালু)
  ===========================================================================
*/

#include <Arduino.h>
#include <math.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ArduinoOTA.h>           // OTA firmware update over WiFi
#include <esp_task_wdt.h>         // Hardware watchdog timer (WDT)


// ===========================================================================
// ★ USER CONFIGURATION – শুধু এই অংশ পরিবর্তন করুন
// ===========================================================================

#define WIFI_SSID    "YOUR_WIFI_NAME"       // ← আপনার WiFi নাম
#define WIFI_PASS    "YOUR_WIFI_PASSWORD"   // ← আপনার WiFi পাসওয়ার্ড

// পিসির IP address যেখানে server.py চলছে
// CMD তে "ipconfig" দিয়ে IPv4 Address দেখুন (e.g. 192.168.1.105)
#define SERVER_IP    "192.168.1.100"
#define SERVER_PORT  5000

// ===========================================================================
// PIN DEFINITIONS
// ===========================================================================

#define PMS_RX_PIN        16    // PMS5003 TXD → ESP32 RX2
#define PMS_TX_PIN        17    // (not wired, required by HardwareSerial)
#define PMS_BAUD_RATE     9600

#define MQ135_PIN         32
#define MQ136_PIN         33
#define MICS_RED_PIN      34
#define MICS_NOX_PIN      35
#define MP135_PIN         36

#define RELAY_FAN_PIN     18    // Relay: HIGH = fan on, LOW = fan off

// ===========================================================================
// ADC & SENSOR CIRCUIT CONSTANTS
// ===========================================================================

const uint8_t  ADC_RESOLUTION_BITS  = 12;
const float    ADC_REF_VOLTAGE      = 3.3f;
const int      ADC_MAX_VALUE        = 4095;
const float    SENSOR_SUPPLY_VOLTAGE = 5.0f;
const float    VOLTAGE_DIVIDER_RATIO = 1.0f;  // 1.0 = no divider

// Load resistor values (kOhm) – hobbyist breakout board defaults
const float MQ135_RL_KOHM    = 20.0f;
const float MQ136_RL_KOHM    = 20.0f;
const float MICS_RED_RL_KOHM = 10.0f;
const float MICS_NOX_RL_KOHM = 10.0f;
const float MP135_RL_KOHM    = 20.0f;

// Gas curve coefficients  ppm = A * (Rs/R0)^B
const float MQ135_CO2_A   = 116.6020682f,  MQ135_CO2_B   = -2.769034857f;
const float MQ135_NH3_A   = 102.694f,      MQ135_NH3_B   = -2.48818f;
const float MQ136_H2S_A   = 40.0f,         MQ136_H2S_B   = -1.7f;
const float MICS_CO_A     = 4.4f,          MICS_CO_B     = -1.4f;
const float MICS_NO2_A    = 0.85f,         MICS_NO2_B    = 1.3f;
const float MP135_VOC_A   = 5.0f,          MP135_VOC_B   = -1.2f;

// Temperature / humidity (fixed; upgrade to BME280 for live values)
const float ASSUMED_TEMP_C   = 25.0f;
const float ASSUMED_HUMID_PCT= 65.0f;

// ===========================================================================
// PMS5003 CONSTANTS
// ===========================================================================

const uint8_t  PMS_PACKET_SIZE   = 32;
const uint8_t  PMS_START_BYTE_1  = 0x42;
const uint8_t  PMS_START_BYTE_2  = 0x4D;
const unsigned long PMS_TIMEOUT_MS = 1500;

// ===========================================================================
// TIMING
// ===========================================================================

const uint16_t     CALIBRATION_SAMPLES  = 50;
const unsigned long CAL_INTERVAL_MS     = 100;
const unsigned long LOOP_INTERVAL_MS    = 2000;   // sensor + transmit every 2 s

// ===========================================================================
// DATA STRUCTURES
// ===========================================================================

enum PMSStatus { PMS_OK, PMS_NOT_DETECTED, PMS_INVALID_HEADER, PMS_CHECKSUM_ERR, PMS_WAITING };

struct PMSData {
  uint16_t pm1_0    = 0;
  uint16_t pm2_5    = 0;
  uint16_t pm10     = 0;
  uint16_t cnt0_3   = 0;
  uint16_t cnt0_5   = 0;
  uint16_t cnt1_0   = 0;
  uint16_t cnt2_5   = 0;
  uint16_t cnt5_0   = 0;
  uint16_t cnt10_0  = 0;
};

struct AQIBreakpoint { float cLow, cHigh; int iLow, iHigh; };
const AQIBreakpoint AQI_BP[7] = {
  {  0.0f,  12.0f,   0,  50},
  { 12.1f,  35.4f,  51, 100},
  { 35.5f,  55.4f, 101, 150},
  { 55.5f, 150.4f, 151, 200},
  {150.5f, 250.4f, 201, 300},
  {250.5f, 350.4f, 301, 400},
  {350.5f, 500.4f, 401, 500}
};

// ===========================================================================
// GLOBAL STATE
// ===========================================================================

HardwareSerial PMS(2);

uint8_t   pmsBuffer[PMS_PACKET_SIZE];
PMSStatus pmsStatus = PMS_WAITING;
PMSData   pmsData;

int   mq135Raw = 0, mq136Raw = 0;
int   micsRedRaw = 0, micsNoxRaw = 0, mp135Raw = 0;

float mq135R0 = 1.0f, mq136R0 = 1.0f;
float micsRedR0 = 1.0f, micsNoxR0 = 1.0f, mp135R0 = 1.0f;
bool  calValid = false;

float estCO2 = 0, estNH3 = 0, estH2S = 0;
float estCO  = 0, estNO2 = 0, estVOC = 0;

bool fanOn = false;
unsigned long lastLoop = 0;

// WiFi / HTTP
String serverUrl;
bool   wifiOk = false;

// WiFi auto-reconnect: exponential backoff (2s → 4s → 8s → … max 64s)
const uint32_t WIFI_RETRY_MIN_MS  = 2000UL;
const uint32_t WIFI_RETRY_MAX_MS  = 64000UL;
uint32_t       wifiRetryDelay     = WIFI_RETRY_MIN_MS;
unsigned long  wifiLastAttempt    = 0;

// OTA hostname (shows in Arduino IDE "Tools > Port")
#define OTA_HOSTNAME  "NirmalNode-ESP32"
#define OTA_PASSWORD  "nirmalnode"   // ← change before deployment

// Hardware Watchdog: reboot if loop hangs for > 30 s
#define WDT_TIMEOUT_SEC  30


// ===========================================================================
// FUNCTION PROTOTYPES
// ===========================================================================

void    connectWiFi();
void    calibrateSensors();
void    readPMS5003();
void    readGasSensors();
int     calcAQI(float pm25);
const char* aqiCategory(int aqi);
float   calcRs(int adc, float rl);
float   estPPM(float ratio, float a, float b);
float   tempHumCorr(float ratio);
void    sendToServer();
void    checkServerCommands();
void    printSerial();

// ===========================================================================
// SETUP
// ===========================================================================

void setup() {
  Serial.begin(115200);
  Serial.println(F("\n[NirmalNode] Booting..."));

  // Fan relay pin
  pinMode(RELAY_FAN_PIN, OUTPUT);
  digitalWrite(RELAY_FAN_PIN, LOW);

  // PMS5003 UART
  PMS.begin(PMS_BAUD_RATE, SERIAL_8N1, PMS_RX_PIN, PMS_TX_PIN);

  // ADC
  analogReadResolution(ADC_RESOLUTION_BITS);
  analogSetAttenuation(ADC_11db);

  // WiFi connection
  connectWiFi();

  // Build server URL once
  serverUrl = String("http://") + SERVER_IP + ":" + SERVER_PORT + "/api/ingest";

  // ----- OTA update -----
  ArduinoOTA.setHostname(OTA_HOSTNAME);
  ArduinoOTA.setPassword(OTA_PASSWORD);
  ArduinoOTA.onStart([]() {
    Serial.println(F("[OTA] Starting firmware update…"));
    digitalWrite(RELAY_FAN_PIN, LOW);   // Safety: turn fan off during OTA
  });
  ArduinoOTA.onEnd([]()   { Serial.println(F("[OTA] Update complete. Rebooting…")); });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("[OTA] Progress: %u%%\r", progress * 100 / total);
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("[OTA] Error[%u]: ", error);
    if      (error == OTA_AUTH_ERROR)    Serial.println(F("Auth Failed"));
    else if (error == OTA_BEGIN_ERROR)   Serial.println(F("Begin Failed"));
    else if (error == OTA_CONNECT_ERROR) Serial.println(F("Connect Failed"));
    else if (error == OTA_RECEIVE_ERROR) Serial.println(F("Receive Failed"));
    else if (error == OTA_END_ERROR)     Serial.println(F("End Failed"));
  });
  if (wifiOk) ArduinoOTA.begin();
  Serial.printf("[OTA] Hostname: %s  (Arduino IDE → Tools → Port)\n", OTA_HOSTNAME);

  // ----- Hardware Watchdog -----
  esp_task_wdt_config_t wdt_cfg = {
      .timeout_ms = WDT_TIMEOUT_SEC * 1000,
      .idle_core_mask = 0,
      .trigger_panic = true
  };
  esp_task_wdt_reconfigure(&wdt_cfg);
  esp_task_wdt_add(NULL);   // subscribe current task
  Serial.printf("[WDT] Hardware watchdog enabled (%d s)\n", WDT_TIMEOUT_SEC);

  // Clean-air baseline calibration
  Serial.println(F("[CAL] Keep sensors in clean air for baseline calibration..."));
  calibrateSensors();

  Serial.println(F("[NirmalNode] Ready! Sending data every 2 seconds."));
  Serial.println(F("=========================================================="));
}

// ===========================================================================
// LOOP
// ===========================================================================

void loop() {
  unsigned long now = millis();

  // ----- Feed hardware watchdog -----
  esp_task_wdt_reset();

  // ----- Handle OTA -----
  ArduinoOTA.handle();

  // ----- WiFi auto-reconnect with exponential backoff -----
  if (WiFi.status() != WL_CONNECTED) {
    wifiOk = false;
    if (now - wifiLastAttempt >= wifiRetryDelay) {
      wifiLastAttempt = now;
      Serial.printf("[WiFi] Disconnected! Reconnecting (backoff=%lus)…\n",
                    wifiRetryDelay / 1000);
      WiFi.disconnect(true);
      WiFi.begin(WIFI_SSID, WIFI_PASS);
      unsigned long t0 = millis();
      while (WiFi.status() != WL_CONNECTED && millis() - t0 < 8000) {
        delay(200);
        esp_task_wdt_reset();  // feed WDT while waiting
      }
      if (WiFi.status() == WL_CONNECTED) {
        wifiOk = true;
        wifiRetryDelay = WIFI_RETRY_MIN_MS;  // reset backoff on success
        Serial.printf("[WiFi] Reconnected! IP: %s\n", WiFi.localIP().toString().c_str());
        ArduinoOTA.begin();   // restart OTA after reconnect
      } else {
        // Exponential backoff: double delay up to max
        wifiRetryDelay = min(wifiRetryDelay * 2, WIFI_RETRY_MAX_MS);
        Serial.printf("[WiFi] Retry failed. Next attempt in %lu s\n",
                      wifiRetryDelay / 1000);
      }
    }
  } else {
    wifiOk = true;
  }

  // ----- Periodic sensor read + transmit -----
  if (now - lastLoop < LOOP_INTERVAL_MS) return;
  lastLoop = now;

  readPMS5003();
  readGasSensors();
  printSerial();          // Always print to Serial Monitor
  sendToServer();         // HTTP POST to server.py
  checkServerCommands();  // Check if server sent FAN_ON / FAN_OFF over Serial
}



// ===========================================================================
// WiFi Connection
// ===========================================================================

void connectWiFi() {
  Serial.printf("[WiFi] Connecting to \"%s\" ", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    wifiOk = true;
    Serial.println(F(" CONNECTED!"));
    Serial.print(F("[WiFi] ESP32 IP Address: "));
    Serial.println(WiFi.localIP());
  } else {
    wifiOk = false;
    Serial.println(F("\n[WiFi] FAILED! Running in Serial-only mode."));
    Serial.println(F("[WiFi] Check WIFI_SSID and WIFI_PASS in the sketch."));
  }
}

// ===========================================================================
// Sensor Calibration (R0 baseline in clean air)
// ===========================================================================

void calibrateSensors() {
  float s135 = 0, s136 = 0, sRed = 0, sNox = 0, s135p = 0;

  for (uint16_t i = 0; i < CALIBRATION_SAMPLES; i++) {
    s135  += calcRs(analogRead(MQ135_PIN),    MQ135_RL_KOHM);
    s136  += calcRs(analogRead(MQ136_PIN),    MQ136_RL_KOHM);
    sRed  += calcRs(analogRead(MICS_RED_PIN), MICS_RED_RL_KOHM);
    sNox  += calcRs(analogRead(MICS_NOX_PIN), MICS_NOX_RL_KOHM);
    s135p += calcRs(analogRead(MP135_PIN),    MP135_RL_KOHM);
    delay(CAL_INTERVAL_MS);
  }

  mq135R0   = s135  / CALIBRATION_SAMPLES;
  mq136R0   = s136  / CALIBRATION_SAMPLES;
  micsRedR0 = sRed  / CALIBRATION_SAMPLES;
  micsNoxR0 = sNox  / CALIBRATION_SAMPLES;
  mp135R0   = s135p / CALIBRATION_SAMPLES;

  calValid = (mq135R0 > 0 && mq136R0 > 0 && micsRedR0 > 0 && micsNoxR0 > 0 && mp135R0 > 0);

  Serial.printf("[CAL] R0: MQ135=%.2f  MQ136=%.2f  RED=%.2f  NOX=%.2f  MP135=%.2f kOhm\n",
                mq135R0, mq136R0, micsRedR0, micsNoxR0, mp135R0);
  if (!calValid) Serial.println(F("[CAL] WARNING: Invalid baseline! Check wiring."));
  else Serial.println(F("[CAL] Calibration OK."));
}

// ===========================================================================
// Rs calculation from ADC
// ===========================================================================

float calcRs(int adc, float rl) {
  float vAdc    = (adc * ADC_REF_VOLTAGE) / ADC_MAX_VALUE;
  float vSensor = vAdc / VOLTAGE_DIVIDER_RATIO;
  if (vSensor < 0.01f) vSensor = 0.01f;
  if (vSensor > SENSOR_SUPPLY_VOLTAGE) vSensor = SENSOR_SUPPLY_VOLTAGE;
  float rs = ((SENSOR_SUPPLY_VOLTAGE - vSensor) / vSensor) * rl;
  return rs < 0 ? 0 : rs;
}

// ppm = A * (Rs/R0)^B
float estPPM(float ratio, float a, float b) {
  if (ratio <= 0) return 0;
  return a * powf(ratio, b);
}

// MQ temperature/humidity correction (MQ135 datasheet ref: 20°C, 65% RH)
float tempHumCorr(float ratio) {
  float t = ASSUMED_TEMP_C, h = ASSUMED_HUMID_PCT;
  float cf = (0.00035f * t * t) - (0.02718f * t) + 1.39538f - ((h - 33.0f) * 0.0018f);
  if (cf < 0.01f) cf = 0.01f;
  return ratio / cf;
}

// ===========================================================================
// Read Gas Sensors
// ===========================================================================

void readGasSensors() {
  mq135Raw = analogRead(MQ135_PIN);
  mq136Raw = analogRead(MQ136_PIN);
  micsRedRaw = analogRead(MICS_RED_PIN);
  micsNoxRaw = analogRead(MICS_NOX_PIN);
  mp135Raw   = analogRead(MP135_PIN);

  if (!calValid) return;

  float r135  = tempHumCorr(calcRs(mq135Raw,   MQ135_RL_KOHM)    / mq135R0);
  float r136  = tempHumCorr(calcRs(mq136Raw,   MQ136_RL_KOHM)    / mq136R0);
  float rRed  = calcRs(micsRedRaw, MICS_RED_RL_KOHM) / micsRedR0;
  float rNox  = calcRs(micsNoxRaw, MICS_NOX_RL_KOHM) / micsNoxR0;
  float rVoc  = calcRs(mp135Raw,   MP135_RL_KOHM)     / mp135R0;

  estCO2 = estPPM(r135, MQ135_CO2_A, MQ135_CO2_B);
  estNH3 = estPPM(r135, MQ135_NH3_A, MQ135_NH3_B);
  estH2S = estPPM(r136, MQ136_H2S_A, MQ136_H2S_B);
  estCO  = estPPM(rRed, MICS_CO_A,   MICS_CO_B);
  estNO2 = estPPM(rNox, MICS_NO2_A,  MICS_NO2_B);
  estVOC = estPPM(rVoc, MP135_VOC_A,  MP135_VOC_B);
}

// ===========================================================================
// Read PMS5003
// ===========================================================================

void readPMS5003() {
  unsigned long t0 = millis();
  bool seen = false;
  uint8_t idx = 0;

  while (millis() - t0 < PMS_TIMEOUT_MS) {
    if (!PMS.available()) continue;
    uint8_t b = (uint8_t)PMS.read();
    seen = true;
    if (idx == 0) {
      if (b == PMS_START_BYTE_1) pmsBuffer[idx++] = b;
    } else if (idx == 1) {
      if (b == PMS_START_BYTE_2) pmsBuffer[idx++] = b;
      else idx = 0;
    } else {
      if (idx < PMS_PACKET_SIZE) pmsBuffer[idx++] = b;
      if (idx >= PMS_PACKET_SIZE) break;
    }
  }

  if (!seen)              { pmsStatus = PMS_NOT_DETECTED; return; }
  if (idx < PMS_PACKET_SIZE) { pmsStatus = PMS_WAITING;      return; }
  if (pmsBuffer[0] != PMS_START_BYTE_1 || pmsBuffer[1] != PMS_START_BYTE_2) {
    pmsStatus = PMS_INVALID_HEADER; return;
  }

  uint16_t sum = 0;
  for (uint8_t i = 0; i < PMS_PACKET_SIZE - 2; i++) sum += pmsBuffer[i];
  uint16_t rxSum = ((uint16_t)pmsBuffer[30] << 8) | pmsBuffer[31];
  if (sum != rxSum) { pmsStatus = PMS_CHECKSUM_ERR; return; }

  pmsData.pm1_0   = ((uint16_t)pmsBuffer[10] << 8) | pmsBuffer[11];
  pmsData.pm2_5   = ((uint16_t)pmsBuffer[12] << 8) | pmsBuffer[13];
  pmsData.pm10    = ((uint16_t)pmsBuffer[14] << 8) | pmsBuffer[15];
  pmsData.cnt0_3  = ((uint16_t)pmsBuffer[16] << 8) | pmsBuffer[17];
  pmsData.cnt0_5  = ((uint16_t)pmsBuffer[18] << 8) | pmsBuffer[19];
  pmsData.cnt1_0  = ((uint16_t)pmsBuffer[20] << 8) | pmsBuffer[21];
  pmsData.cnt2_5  = ((uint16_t)pmsBuffer[22] << 8) | pmsBuffer[23];
  pmsData.cnt5_0  = ((uint16_t)pmsBuffer[24] << 8) | pmsBuffer[25];
  pmsData.cnt10_0 = ((uint16_t)pmsBuffer[26] << 8) | pmsBuffer[27];
  pmsStatus = PMS_OK;
}

// ===========================================================================
// AQI Calculation (US EPA PM2.5)
// ===========================================================================

int calcAQI(float pm25) {
  float c = floorf(pm25 * 10.0f) / 10.0f;
  if (c < 0) c = 0;
  if (c > 500.4f) c = 500.4f;
  for (uint8_t i = 0; i < 7; i++) {
    if (c >= AQI_BP[i].cLow && c <= AQI_BP[i].cHigh) {
      return (int)roundf(((float)(AQI_BP[i].iHigh - AQI_BP[i].iLow)
              / (AQI_BP[i].cHigh - AQI_BP[i].cLow))
              * (c - AQI_BP[i].cLow) + AQI_BP[i].iLow);
    }
  }
  return 500;
}

const char* aqiCategory(int aqi) {
  if (aqi <= 50)  return "Good";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 150) return "Unhealthy for Sensitive Groups";
  if (aqi <= 200) return "Unhealthy";
  if (aqi <= 300) return "Very Unhealthy";
  return "Hazardous";
}

// ===========================================================================
// HTTP POST → server.py /api/ingest
// ===========================================================================

void sendToServer() {
  if (!wifiOk) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println(F("[WiFi] Reconnecting..."));
      WiFi.reconnect();
      return;
    }
    wifiOk = true;
  }

  // Build compact JSON payload
  StaticJsonDocument<512> doc;
  doc["pm1_0"]        = pmsStatus == PMS_OK ? pmsData.pm1_0  : 0;
  doc["pm2_5"]        = pmsStatus == PMS_OK ? pmsData.pm2_5  : 0;
  doc["pm10"]         = pmsStatus == PMS_OK ? pmsData.pm10   : 0;
  doc["cnt0_3"]       = pmsStatus == PMS_OK ? pmsData.cnt0_3 : 0;
  doc["cnt0_5"]       = pmsStatus == PMS_OK ? pmsData.cnt0_5 : 0;
  doc["cnt1_0"]       = pmsStatus == PMS_OK ? pmsData.cnt1_0 : 0;
  doc["cnt2_5"]       = pmsStatus == PMS_OK ? pmsData.cnt2_5 : 0;
  doc["cnt5_0"]       = pmsStatus == PMS_OK ? pmsData.cnt5_0 : 0;
  doc["cnt10_0"]      = pmsStatus == PMS_OK ? pmsData.cnt10_0: 0;
  doc["mq135_adc"]    = mq135Raw;
  doc["mq136_adc"]    = mq136Raw;
  doc["mics_red_adc"] = micsRedRaw;
  doc["mics_nox_adc"] = micsNoxRaw;
  doc["mp135_adc"]    = mp135Raw;
  if (calValid) {
    doc["co2_est"]  = serialized(String(estCO2, 1));
    doc["nh3_est"]  = serialized(String(estNH3, 2));
    doc["h2s_est"]  = serialized(String(estH2S, 2));
    doc["co_est"]   = serialized(String(estCO,  1));
    doc["no2_est"]  = serialized(String(estNO2, 2));
    doc["voc_est"]  = serialized(String(estVOC, 1));
  }
  doc["pms_ok"]  = (pmsStatus == PMS_OK);
  doc["cal_ok"]  = calValid;
  doc["fan"]     = fanOn;

  char payload[512];
  serializeJson(doc, payload);

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(payload);

  if (code == 200) {
    // Check if server replied with FAN command
    String resp = http.getString();
    if (resp.indexOf("FAN_ON") >= 0) {
      fanOn = true;
      digitalWrite(RELAY_FAN_PIN, HIGH);
      Serial.println(F("[FAN] Server commanded: FAN ON"));
    } else if (resp.indexOf("FAN_OFF") >= 0) {
      fanOn = false;
      digitalWrite(RELAY_FAN_PIN, LOW);
      Serial.println(F("[FAN] Server commanded: FAN OFF"));
    }
    Serial.printf("[HTTP] POST OK (%d ms)\n", http.getSize());
  } else {
    Serial.printf("[HTTP] POST failed: %d\n", code);
  }

  http.end();
}

// ===========================================================================
// Check Serial for manual commands (FAN_ON / FAN_OFF from Serial Monitor)
// ===========================================================================

void checkServerCommands() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd == "FAN_ON") {
    fanOn = true;
    digitalWrite(RELAY_FAN_PIN, HIGH);
    Serial.println(F("[FAN] Manual: FAN ON"));
  } else if (cmd == "FAN_OFF") {
    fanOn = false;
    digitalWrite(RELAY_FAN_PIN, LOW);
    Serial.println(F("[FAN] Manual: FAN OFF"));
  } else if (cmd == "STATUS") {
    Serial.printf("[STATUS] WiFi=%s  IP=%s  Fan=%s\n",
      WiFi.status() == WL_CONNECTED ? "OK" : "FAIL",
      WiFi.localIP().toString().c_str(),
      fanOn ? "ON" : "OFF");
  }
}

// ===========================================================================
// Serial Monitor Print (debug)
// ===========================================================================

void printSerial() {
  Serial.println(F("----------------------------------------------"));
  Serial.printf("[PMS] PM1.0=%u  PM2.5=%u  PM10=%u ug/m3  [%s]\n",
    pmsData.pm1_0, pmsData.pm2_5, pmsData.pm10,
    pmsStatus == PMS_OK ? "OK" : "WAIT");
  Serial.printf("[GAS] MQ135=%d  MQ136=%d  RED=%d  NOX=%d  MP135=%d\n",
    mq135Raw, mq136Raw, micsRedRaw, micsNoxRaw, mp135Raw);
  if (calValid) {
    Serial.printf("[EST] CO2=%.1f  CO=%.1f  NO2=%.2f  NH3=%.2f  H2S=%.2f  VOC=%.1f ppm\n",
      estCO2, estCO, estNO2, estNH3, estH2S, estVOC);
  }
  if (pmsStatus == PMS_OK) {
    int aqi = calcAQI(pmsData.pm2_5);
    Serial.printf("[AQI] %d - %s  |  Fan: %s\n", aqi, aqiCategory(aqi), fanOn ? "ON" : "off");
  }
  Serial.printf("[NET] WiFi=%s  Server=%s\n",
    wifiOk ? "OK" : "FAIL", serverUrl.c_str());
  Serial.println(F("----------------------------------------------"));
}
