/*
  ===========================================================================
  AirGuard – Air Quality Monitoring System  [WiFi + NirmalNode AI Edition]
  ---------------------------------------------------------------------------
  BOARD            : ESP32 DevKit V1 (ESP-WROOM-32, 30-pin)
  CORE             : ESP32 Arduino Core 3.x

  SENSORS
    PMS5003       (UART2)      - Particulate Matter + Particle Counts
    MQ135         (GPIO32)     - CO2 / NH3 (ppm)
    MQ136         (GPIO33)     - H2S (ppm)
    MiCS-4514 RED (GPIO34)     - CO (ppm)
    MiCS-4514 NOX (GPIO35)     - NO2 (ppm)
    MP135         (GPIO36/VP)  - VOC index

  NEW ADDITIONS:
    WiFi          (built-in)   - Sends JSON to NirmalNode server.py every 2s
    Fan Relay     (GPIO25/D25) - HIGH = fan ON, LOW = fan OFF
                                 Controlled by AI ML engine via HTTP response

  ★ QUICK SETUP – শুধু এই ৩টা লাইন বদলান:
     #define WIFI_SSID   "আপনার WiFi নাম"
     #define WIFI_PASS   "আপনার WiFi পাসওয়ার্ড"
     #define SERVER_IP   "পিসির IP"  (CMD → ipconfig → IPv4 Address)
  ===========================================================================
*/

/*
  ===========================================================================
  DEMO MODE
  ---------------------------------------------------------------------------
  Set DEMO_MODE to 1 to develop/test the UI (Serial report, dashboards, etc.)
  while the PMS5003 and MiCS-4514 are unstable / disconnected.

    DEMO_MODE = 1  -> PM1.0/PM2.5/PM10 are NOT generated independently.
                       They are driven by the real, live MQ135 and MP135
                       readings only: each cycle, MQ135's and MP135's actual
                       Rs/R0 ratio is compared against a "normal" band
                       (matches the clean-air calibration baseline). If BOTH
                       are inside that normal band, PM stays near the LOW end
                       of its range. If EITHER one drifts abnormal, PM rises
                       toward the HIGH end of its range (up to the max, e.g.
                       PM10 -> 250). Light smoothing keeps the transition
                       gradual instead of jumping every cycle. MiCS RED/NOX
                       raw ADC values are likewise derived from the still-
                       working MQ135 / MQ136 / MP135 sensors (not free-
                       floating). Everything downstream (Rs/R0, ppm curves,
                       AQI) runs through the exact same code path as real
                       hardware would use.

    DEMO_MODE = 0  -> Original behavior: real PMS5003 UART parsing and real
                       MiCS-4514 analogRead() calls. Nothing else changes.

  All original PMS5003 / MiCS-4514 code is preserved untouched inside
  '#else' branches - flipping this single flag is the only thing needed to
  switch back to real hardware.
  ===========================================================================
*/
#define DEMO_MODE 1

#include <Arduino.h>
#include <math.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===========================================================================
// ★ WiFi & Server Configuration – শুধু এই ৩টা লাইন পরিবর্তন করুন
// ===========================================================================

#define WIFI_SSID   "YOUR_WIFI_NAME"        // ← আপনার WiFi নাম
#define WIFI_PASS   "YOUR_WIFI_PASSWORD"    // ← আপনার WiFi পাসওয়ার্ড
#define SERVER_IP   "192.168.1.100"         // ← পিসির IP (CMD → ipconfig)
#define SERVER_PORT 5000

// ===========================================================================
// SECTION: Pin Definitions
// ===========================================================================

// ---- PMS5003 (UART2) ----
#define PMS_RX_PIN        16   // ESP32 RX2 <- PMS5003 TXD
#define PMS_TX_PIN        17   // Required by HardwareSerial API, not wired
#define PMS_BAUD_RATE     9600

// ---- Gas Sensors (Analog, ADC1 channels) ----
#define MQ135_PIN         32
#define MQ136_PIN         33
#define MICS_RED_PIN      34
#define MICS_NOX_PIN      35
#define MP135_PIN         36

// ---- Fan / Purifier Relay ----
#define RELAY_FAN_PIN     25   // D25 → Relay IN  (HIGH = ON, LOW = OFF)

// ===========================================================================
// SECTION: ADC Configuration
// ===========================================================================

const uint8_t  ADC_RESOLUTION_BITS = 12;        // 0 - 4095
const adc_attenuation_t ADC_ATTEN  = ADC_11db;   // Full ~0 - 3.3V input range
const float    ADC_REF_VOLTAGE     = 3.3f;
const int      ADC_MAX_VALUE       = 4095;

// ===========================================================================
// SECTION: Gas Sensor Circuit Constants
// ===========================================================================

const float SENSOR_SUPPLY_VOLTAGE = 5.0f;
const float VOLTAGE_DIVIDER_RATIO = 1.0f;

const float MQ135_RL_KOHM     = 20.0f;
const float MQ136_RL_KOHM     = 20.0f;
const float MICS_RED_RL_KOHM  = 10.0f;
const float MICS_NOX_RL_KOHM  = 10.0f;
const float MP135_RL_KOHM     = 20.0f;

// ===========================================================================
// SECTION: Gas Curve Coefficients (ppm = a * (Rs/R0)^b)
// ===========================================================================

const float MQ135_CO2_CURVE_A = 116.6020682f;
const float MQ135_CO2_CURVE_B = -2.769034857f;

const float MQ135_NH3_CURVE_A = 102.694f;
const float MQ135_NH3_CURVE_B = -2.48818f;

const float MQ136_H2S_CURVE_A = 40.0f;
const float MQ136_H2S_CURVE_B = -1.7f;

const float MICS_RED_CO_CURVE_A = 4.4f;
const float MICS_RED_CO_CURVE_B = -1.4f;

const float MICS_NOX_NO2_CURVE_A = 0.85f;
const float MICS_NOX_NO2_CURVE_B = 1.3f;

const float MP135_VOC_CURVE_A = 5.0f;
const float MP135_VOC_CURVE_B = -1.2f;

// ===========================================================================
// SECTION: Temperature / Humidity Compensation (fixed assumed values)
// ===========================================================================

const float ASSUMED_TEMPERATURE_C    = 20.0f;
const float ASSUMED_HUMIDITY_PERCENT = 65.0f;

// ===========================================================================
// SECTION: PMS5003 Protocol Constants
// ===========================================================================

const uint8_t PMS_PACKET_SIZE  = 32;
const uint8_t PMS_START_BYTE_1 = 0x42;
const uint8_t PMS_START_BYTE_2 = 0x4D;
const unsigned long PMS_READ_TIMEOUT_MS = 1500;

// ===========================================================================
// SECTION: Calibration & Timing Constants
// ===========================================================================

const uint16_t CALIBRATION_SAMPLE_COUNT     = 50;
const unsigned long CALIBRATION_INTERVAL_MS = 100;
const unsigned long LOOP_DELAY_MS           = 2000;

// ===========================================================================
// SECTION: Global Objects
// ===========================================================================

HardwareSerial PMS(2); // UART2 dedicated to PMS5003

// ===========================================================================
// SECTION: Data Structures
// ===========================================================================

enum PMSStatus {
  PMS_STATUS_OK,
  PMS_STATUS_NOT_DETECTED,
  PMS_STATUS_INVALID_HEADER,
  PMS_STATUS_CHECKSUM_ERROR,
  PMS_STATUS_WAITING
};

struct PMSData {
  uint16_t pm1_0     = 0;
  uint16_t pm2_5     = 0;
  uint16_t pm10      = 0;
  uint16_t count0_3  = 0;
  uint16_t count0_5  = 0;
  uint16_t count1_0  = 0;
  uint16_t count2_5  = 0;
  uint16_t count5_0  = 0;
  uint16_t count10_0 = 0;
};

struct AQIBreakpoint {
  float concLow;
  float concHigh;
  int   aqiLow;
  int   aqiHigh;
};

const AQIBreakpoint PM25_BREAKPOINTS[7] = {
  {  0.0f,  12.0f,   0,  50 },
  { 12.1f,  35.4f,  51, 100 },
  { 35.5f,  55.4f, 101, 150 },
  { 55.5f, 150.4f, 151, 200 },
  {150.5f, 250.4f, 201, 300 },
  {250.5f, 350.4f, 301, 400 },
  {350.5f, 500.4f, 401, 500 }
};

// ===========================================================================
// SECTION: Global State
// ===========================================================================

uint8_t   pmsBuffer[PMS_PACKET_SIZE];
PMSStatus pmsStatus = PMS_STATUS_WAITING;
PMSData   pmsData;

int mq135RawADC   = 0;
int mq136RawADC   = 0;
int micsRedRawADC = 0;
int micsNoxRawADC = 0;
int mp135RawADC   = 0;

float mq135R0     = 0.0f;
float mq136R0     = 0.0f;
float micsRedR0   = 0.0f;
float micsNoxR0   = 0.0f;
float mp135R0     = 0.0f;
bool  calibrationValid = false;

float mq135RsKOhm   = 0.0f;
float mq135RsRatio  = 0.0f;
float estimatedCO2  = 0.0f;
float estimatedNH3  = 0.0f;

float mq136RsKOhm   = 0.0f;
float mq136RsRatio  = 0.0f;
float estimatedH2S  = 0.0f;

float micsRedRsKOhm  = 0.0f;
float micsRedRsRatio = 0.0f;
float estimatedCO    = 0.0f;

float micsNoxRsKOhm  = 0.0f;
float micsNoxRsRatio = 0.0f;
float estimatedNO2   = 0.0f;

float mp135RsKOhm   = 0.0f;
float mp135RsRatio  = 0.0f;
float estimatedVOC  = 0.0f;

int         currentAQI = 0;
const char* currentAQICategory = "N/A";

// ---- WiFi / Fan state ----
bool fanOn   = false;
bool wifiOk  = false;
String serverUrl;

// ===========================================================================
// FUNCTION PROTOTYPES
// ===========================================================================

void        connectWiFi();
void        sendToServer();
void        checkSerialCommands();
void        setFan(bool on);

void        readPMS5003();
void        readGasSensors();
void        calibrateSensors();
float       calculateRs(int adcRaw, float rlKOhm);
float       estimatePPM(float rsRatio, float curveA, float curveB);
float       readAmbientTemperature();
float       readAmbientHumidity();
float       applyTempHumidityCorrection(float rsRatio, float temperatureC, float humidityPercent);
int         calculateAQI(float pm25);
const char* getAQICategory(int aqi);
void        printReport();

#if DEMO_MODE
float       ratioToAbnormalFactor(float rsRatio);
float       calculatePollutionIndex();
float       mapIndexToRange(float index, float minVal, float maxVal);
float       applySmallJitter(float value, float rangeSpan, float &noiseState);
void        generateDemoPMSData();
int         simulateMicsRedADC();
int         simulateMicsNoxADC();
#endif

// ===========================================================================
// SETUP
// ===========================================================================

void setup() {
  Serial.begin(115200);

  randomSeed(micros());

  // ---- Fan relay pin ----
  pinMode(RELAY_FAN_PIN, OUTPUT);
  digitalWrite(RELAY_FAN_PIN, LOW);   // Fan off at boot
  fanOn = false;

  // ---- PMS5003 UART2 ----
  PMS.begin(PMS_BAUD_RATE, SERIAL_8N1, PMS_RX_PIN, PMS_TX_PIN);

  // ---- ADC Configuration ----
  analogReadResolution(ADC_RESOLUTION_BITS);
  analogSetPinAttenuation(MQ135_PIN,    ADC_ATTEN);
  analogSetPinAttenuation(MQ136_PIN,    ADC_ATTEN);
  analogSetPinAttenuation(MICS_RED_PIN, ADC_ATTEN);
  analogSetPinAttenuation(MICS_NOX_PIN, ADC_ATTEN);
  analogSetPinAttenuation(MP135_PIN,    ADC_ATTEN);

  Serial.println();
  Serial.println(F("======================================================"));
  Serial.println(F("AirGuard + NirmalNode AI  [WiFi Edition]"));
  Serial.println(F("======================================================"));

  // ---- WiFi ----
  connectWiFi();

  serverUrl = String("http://") + SERVER_IP + ":" + SERVER_PORT + "/api/ingest";
  Serial.print(F("[NET] Server URL: "));
  Serial.println(serverUrl);

  // ---- Sensor Calibration ----
  Serial.println(F("[CAL] Calibrating sensors in ambient air, please wait..."));
  calibrateSensors();
}

// ===========================================================================
// LOOP
// ===========================================================================

void loop() {
  // NOTE: order matters in DEMO_MODE — readGasSensors() must run first so
  // fresh MQ135/MP135 readings are available when generateDemoPMSData() runs.
  readGasSensors();
  readPMS5003();
  printReport();
  sendToServer();           // HTTP POST → server.py → ML engine → fan cmd
  checkSerialCommands();    // FAN_ON / FAN_OFF / STATUS via Serial Monitor

  delay(LOOP_DELAY_MS);
}

// ===========================================================================
// WiFi Connection
// ===========================================================================

void connectWiFi() {
  Serial.printf("[WiFi] Connecting to \"%s\" ", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  uint8_t tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 30) {
    delay(500);
    Serial.print(".");
    tries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    wifiOk = true;
    Serial.println(F(" OK!"));
    Serial.print(F("[WiFi] ESP32 IP: "));
    Serial.println(WiFi.localIP());
  } else {
    wifiOk = false;
    Serial.println(F("\n[WiFi] FAILED – check WIFI_SSID / WIFI_PASS"));
    Serial.println(F("[WiFi] Running in Serial-only mode."));
  }
}

// ===========================================================================
// Send Sensor Data to server.py via HTTP POST
// Server responds with {"fan":"FAN_ON"} or {"fan":"FAN_OFF"} based on ML AQI
// ===========================================================================

void sendToServer() {
  // Reconnect if dropped
  if (!wifiOk || WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    delay(500);
    wifiOk = (WiFi.status() == WL_CONNECTED);
    if (!wifiOk) return;
  }

  // Build JSON payload — same field names the ML engine expects
  StaticJsonDocument<512> doc;

  doc["pm1_0"]        = pmsStatus == PMS_STATUS_OK ? (int)pmsData.pm1_0   : 0;
  doc["pm2_5"]        = pmsStatus == PMS_STATUS_OK ? (int)pmsData.pm2_5   : 0;
  doc["pm10"]         = pmsStatus == PMS_STATUS_OK ? (int)pmsData.pm10    : 0;
  doc["cnt0_3"]       = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count0_3: 0;
  doc["cnt0_5"]       = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count0_5: 0;
  doc["cnt1_0"]       = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count1_0: 0;
  doc["cnt2_5"]       = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count2_5: 0;
  doc["cnt5_0"]       = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count5_0: 0;
  doc["cnt10_0"]      = pmsStatus == PMS_STATUS_OK ? (int)pmsData.count10_0:0;

  doc["mq135_adc"]    = mq135RawADC;
  doc["mq136_adc"]    = mq136RawADC;
  doc["mics_red_adc"] = micsRedRawADC;
  doc["mics_nox_adc"] = micsNoxRawADC;
  doc["mp135_adc"]    = mp135RawADC;

  if (calibrationValid) {
    doc["co2_est"] = (float)((int)(estimatedCO2 * 10)) / 10.0f;
    doc["nh3_est"] = (float)((int)(estimatedNH3 * 100)) / 100.0f;
    doc["h2s_est"] = (float)((int)(estimatedH2S * 100)) / 100.0f;
    doc["co_est"]  = (float)((int)(estimatedCO  * 10)) / 10.0f;
    doc["no2_est"] = (float)((int)(estimatedNO2 * 100)) / 100.0f;
    doc["voc_est"] = (float)((int)(estimatedVOC * 10)) / 10.0f;
  }

  doc["pms_ok"]   = (pmsStatus == PMS_STATUS_OK);
  doc["cal_ok"]   = calibrationValid;
  doc["demo"]     = (bool)DEMO_MODE;
  doc["fan"]      = fanOn;

  char payload[512];
  serializeJson(doc, payload);

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(3000);

  int code = http.POST(payload);

  if (code == 200) {
    String resp = http.getString();

    // Parse fan command from server ML response
    StaticJsonDocument<128> respDoc;
    if (!deserializeJson(respDoc, resp)) {
      const char* fanCmd = respDoc["fan"] | "";
      int         aiAqi  = respDoc["aqi"]  | 0;

      if (strcmp(fanCmd, "FAN_ON") == 0) {
        setFan(true);
      } else if (strcmp(fanCmd, "FAN_OFF") == 0) {
        setFan(false);
      }

      Serial.printf("[NET] -> AQI=%d  Fan=%s\n", aiAqi, fanOn ? "ON" : "OFF");
    }
  } else {
    Serial.printf("[NET] POST failed: HTTP %d\n", code);
  }

  http.end();
}

// ===========================================================================
// Fan / Relay Control (D25)
// ===========================================================================

void setFan(bool on) {
  if (fanOn == on) return;   // No change – skip noisy Serial print
  fanOn = on;
  digitalWrite(RELAY_FAN_PIN, on ? HIGH : LOW);
  Serial.printf("[FAN] D25 Relay -> %s\n", on ? "ON (Purifier Active)" : "OFF (Standby)");
}

// ===========================================================================
// Serial Monitor manual commands  (type in Arduino IDE Serial Monitor)
//   FAN_ON   – force fan on
//   FAN_OFF  – force fan off
//   STATUS   – print WiFi + fan state
// ===========================================================================

void checkSerialCommands() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if      (cmd == "FAN_ON")  { setFan(true);  }
  else if (cmd == "FAN_OFF") { setFan(false); }
  else if (cmd == "STATUS") {
    Serial.printf("[STATUS] WiFi=%s  IP=%s  Fan=%s  CalValid=%s  DEMO=%d\n",
      WiFi.status() == WL_CONNECTED ? "OK" : "FAIL",
      WiFi.localIP().toString().c_str(),
      fanOn ? "ON" : "OFF",
      calibrationValid ? "YES" : "NO",
      DEMO_MODE);
  }
}

// ===========================================================================
// FUNCTION: calibrateSensors()
// ===========================================================================

void calibrateSensors() {
  float mq135Sum   = 0.0f;
  float mq136Sum   = 0.0f;
  float micsRedSum = 0.0f;
  float micsNoxSum = 0.0f;
  float mp135Sum   = 0.0f;

  for (uint16_t sample = 0; sample < CALIBRATION_SAMPLE_COUNT; sample++) {
    mq135RawADC = analogRead(MQ135_PIN);
    mq136RawADC = analogRead(MQ136_PIN);
    mp135RawADC = analogRead(MP135_PIN);

#if DEMO_MODE
    micsRedRawADC = simulateMicsRedADC();
    micsNoxRawADC = simulateMicsNoxADC();
#else
    micsRedRawADC = analogRead(MICS_RED_PIN);
    micsNoxRawADC = analogRead(MICS_NOX_PIN);
#endif

    mq135Sum   += calculateRs(mq135RawADC,   MQ135_RL_KOHM);
    mq136Sum   += calculateRs(mq136RawADC,   MQ136_RL_KOHM);
    micsRedSum += calculateRs(micsRedRawADC, MICS_RED_RL_KOHM);
    micsNoxSum += calculateRs(micsNoxRawADC, MICS_NOX_RL_KOHM);
    mp135Sum   += calculateRs(mp135RawADC,   MP135_RL_KOHM);

    delay(CALIBRATION_INTERVAL_MS);
  }

  mq135R0   = mq135Sum   / (float)CALIBRATION_SAMPLE_COUNT;
  mq136R0   = mq136Sum   / (float)CALIBRATION_SAMPLE_COUNT;
  micsRedR0 = micsRedSum / (float)CALIBRATION_SAMPLE_COUNT;
  micsNoxR0 = micsNoxSum / (float)CALIBRATION_SAMPLE_COUNT;
  mp135R0   = mp135Sum   / (float)CALIBRATION_SAMPLE_COUNT;

  calibrationValid = (mq135R0 > 0.0f) && (mq136R0 > 0.0f) &&
                     (micsRedR0 > 0.0f) && (micsNoxR0 > 0.0f) && (mp135R0 > 0.0f);

  Serial.println(F("[CAL] Calibration Complete - Baseline (R0) Values"));
  Serial.printf("  MQ135 R0   : %.2f kOhm\n", mq135R0);
  Serial.printf("  MQ136 R0   : %.2f kOhm\n", mq136R0);
  Serial.printf("  MiCS RED R0: %.2f kOhm\n", micsRedR0);
  Serial.printf("  MiCS NOX R0: %.2f kOhm\n", micsNoxR0);
  Serial.printf("  MP135 R0   : %.2f kOhm\n", mp135R0);
  if (!calibrationValid)
    Serial.println(F("[CAL] WARNING: Invalid baseline! Check sensor wiring."));
  Serial.println(F("======================================================"));
  Serial.println();
}

// ===========================================================================
// FUNCTION: calculateRs()
// ===========================================================================

float calculateRs(int adcRaw, float rlKOhm) {
  float adcVoltage = (adcRaw * ADC_REF_VOLTAGE) / (float)ADC_MAX_VALUE;
  float sensorVoltage = adcVoltage / VOLTAGE_DIVIDER_RATIO;
  if (sensorVoltage < 0.01f) sensorVoltage = 0.01f;
  if (sensorVoltage > SENSOR_SUPPLY_VOLTAGE) sensorVoltage = SENSOR_SUPPLY_VOLTAGE;
  float rs = ((SENSOR_SUPPLY_VOLTAGE - sensorVoltage) / sensorVoltage) * rlKOhm;
  return rs < 0.0f ? 0.0f : rs;
}

// ===========================================================================
// FUNCTION: estimatePPM()
// ===========================================================================

float estimatePPM(float rsRatio, float curveA, float curveB) {
  if (rsRatio <= 0.0f) return 0.0f;
  return curveA * powf(rsRatio, curveB);
}

// ===========================================================================
// FUNCTION: readAmbientTemperature() / readAmbientHumidity()
// ===========================================================================

float readAmbientTemperature() { return ASSUMED_TEMPERATURE_C;    }
float readAmbientHumidity()    { return ASSUMED_HUMIDITY_PERCENT;  }

// ===========================================================================
// FUNCTION: applyTempHumidityCorrection()
// ===========================================================================

float applyTempHumidityCorrection(float rsRatio, float temperatureC, float humidityPercent) {
  float cf = (0.00035f * temperatureC * temperatureC)
             - (0.02718f * temperatureC)
             + 1.39538f
             - ((humidityPercent - 33.0f) * 0.0018f);
  if (cf < 0.01f) cf = 0.01f;
  return rsRatio / cf;
}

// ===========================================================================
// DEMO MODE FUNCTIONS (unchanged from original)
// ===========================================================================

#if DEMO_MODE

const float DEMO_NORMAL_RATIO_THRESHOLD   = 0.85f;
const float DEMO_ABNORMAL_RATIO_THRESHOLD = 0.20f;

float ratioToAbnormalFactor(float rsRatio) {
  if (rsRatio >= DEMO_NORMAL_RATIO_THRESHOLD)   return 0.0f;
  if (rsRatio <= DEMO_ABNORMAL_RATIO_THRESHOLD) return 1.0f;
  return (DEMO_NORMAL_RATIO_THRESHOLD - rsRatio) /
         (DEMO_NORMAL_RATIO_THRESHOLD - DEMO_ABNORMAL_RATIO_THRESHOLD);
}

float calculatePollutionIndex() {
  static float smoothedIndex = 0.0f;
  if (!calibrationValid) return smoothedIndex;

  float mq135Factor = ratioToAbnormalFactor(mq135RsRatio);
  float mp135Factor = ratioToAbnormalFactor(mp135RsRatio);
  float rawIndex    = constrain(max(mq135Factor, mp135Factor), 0.0f, 1.0f);

  smoothedIndex = (smoothedIndex * 0.85f) + (rawIndex * 0.15f);
  return smoothedIndex;
}

float mapIndexToRange(float index, float minVal, float maxVal) {
  return minVal + (constrain(index, 0.0f, 1.0f) * (maxVal - minVal));
}

float applySmallJitter(float value, float rangeSpan, float &noiseState) {
  float rawJitter = ((float)random(-100, 100) / 100.0f) * (rangeSpan * 0.05f);
  noiseState = (noiseState * 0.90f) + (rawJitter * 0.10f);
  return value + noiseState;
}

void generateDemoPMSData() {
  static float noisePM1  = 0.0f;
  static float noisePM25 = 0.0f;
  static float noisePM10 = 0.0f;

  float pollutionIndex = calculatePollutionIndex();

  float pm1  = mapIndexToRange(pollutionIndex,  5.0f,  80.0f);
  float pm25 = mapIndexToRange(pollutionIndex, 10.0f, 150.0f);
  float pm10 = mapIndexToRange(pollutionIndex, 20.0f, 250.0f);

  pm1  = applySmallJitter(pm1,   80.0f -  5.0f, noisePM1);
  pm25 = applySmallJitter(pm25, 150.0f - 10.0f, noisePM25);
  pm10 = applySmallJitter(pm10, 250.0f - 20.0f, noisePM10);

  pm1  = constrain(pm1,   5.0f,  80.0f);
  pm25 = constrain(pm25, 10.0f, 150.0f);
  pm10 = constrain(pm10, 20.0f, 250.0f);

  pmsData.pm1_0 = (uint16_t)roundf(pm1);
  pmsData.pm2_5 = (uint16_t)roundf(pm25);
  pmsData.pm10  = (uint16_t)roundf(pm10);

  if (pmsData.pm2_5 < pmsData.pm1_0) pmsData.pm2_5 = pmsData.pm1_0;
  if (pmsData.pm10  < pmsData.pm2_5) pmsData.pm10  = pmsData.pm2_5;

  pmsData.count0_3  = (uint16_t)(pmsData.pm10 * 18.0f);
  pmsData.count0_5  = (uint16_t)(pmsData.pm10 *  6.0f);
  pmsData.count1_0  = (uint16_t)(pmsData.pm10 *  2.5f);
  pmsData.count2_5  = (uint16_t)(pmsData.pm10 *  0.6f);
  pmsData.count5_0  = (uint16_t)(pmsData.pm10 *  0.15f);
  pmsData.count10_0 = (uint16_t)(pmsData.pm10 *  0.05f);

  pmsStatus = PMS_STATUS_OK;
}

int simulateMicsRedADC() {
  int mp135Sample = analogRead(MP135_PIN);
  int base        = (mq135RawADC + mp135Sample) / 2;
  int noise       = random(-30, 30);
  return constrain(base + noise, 0, ADC_MAX_VALUE);
}

int simulateMicsNoxADC() {
  int base  = (mq136RawADC + mq135RawADC) / 2;
  int noise = random(-30, 30);
  return constrain(base + noise, 0, ADC_MAX_VALUE);
}

#endif // DEMO_MODE

// ===========================================================================
// FUNCTION: readGasSensors()
// ===========================================================================

void readGasSensors() {
  float temperatureC    = readAmbientTemperature();
  float humidityPercent = readAmbientHumidity();

  mq135RawADC  = analogRead(MQ135_PIN);
  mq135RsKOhm  = calculateRs(mq135RawADC, MQ135_RL_KOHM);
  mq135RsRatio = calibrationValid ? applyTempHumidityCorrection(mq135RsKOhm / mq135R0, temperatureC, humidityPercent) : 0.0f;
  estimatedCO2 = calibrationValid ? estimatePPM(mq135RsRatio, MQ135_CO2_CURVE_A, MQ135_CO2_CURVE_B) : 0.0f;
  estimatedNH3 = calibrationValid ? estimatePPM(mq135RsRatio, MQ135_NH3_CURVE_A, MQ135_NH3_CURVE_B) : 0.0f;

  mq136RawADC  = analogRead(MQ136_PIN);
  mq136RsKOhm  = calculateRs(mq136RawADC, MQ136_RL_KOHM);
  mq136RsRatio = calibrationValid ? applyTempHumidityCorrection(mq136RsKOhm / mq136R0, temperatureC, humidityPercent) : 0.0f;
  estimatedH2S = calibrationValid ? estimatePPM(mq136RsRatio, MQ136_H2S_CURVE_A, MQ136_H2S_CURVE_B) : 0.0f;

#if DEMO_MODE
  micsRedRawADC  = simulateMicsRedADC();
#else
  micsRedRawADC  = analogRead(MICS_RED_PIN);
#endif
  micsRedRsKOhm  = calculateRs(micsRedRawADC, MICS_RED_RL_KOHM);
  micsRedRsRatio = calibrationValid ? (micsRedRsKOhm / micsRedR0) : 0.0f;
  estimatedCO    = calibrationValid ? estimatePPM(micsRedRsRatio, MICS_RED_CO_CURVE_A, MICS_RED_CO_CURVE_B) : 0.0f;

#if DEMO_MODE
  micsNoxRawADC  = simulateMicsNoxADC();
#else
  micsNoxRawADC  = analogRead(MICS_NOX_PIN);
#endif
  micsNoxRsKOhm  = calculateRs(micsNoxRawADC, MICS_NOX_RL_KOHM);
  micsNoxRsRatio = calibrationValid ? (micsNoxRsKOhm / micsNoxR0) : 0.0f;
  estimatedNO2   = calibrationValid ? estimatePPM(micsNoxRsRatio, MICS_NOX_NO2_CURVE_A, MICS_NOX_NO2_CURVE_B) : 0.0f;

  mp135RawADC  = analogRead(MP135_PIN);
  mp135RsKOhm  = calculateRs(mp135RawADC, MP135_RL_KOHM);
  mp135RsRatio = calibrationValid ? (mp135RsKOhm / mp135R0) : 0.0f;
  estimatedVOC = calibrationValid ? estimatePPM(mp135RsRatio, MP135_VOC_CURVE_A, MP135_VOC_CURVE_B) : 0.0f;
}

// ===========================================================================
// FUNCTION: readPMS5003()
// ===========================================================================

void readPMS5003() {
#if DEMO_MODE
  generateDemoPMSData();
#else
  unsigned long startTime   = millis();
  bool          anyByteSeen = false;
  uint8_t       index       = 0;

  while ((millis() - startTime) < PMS_READ_TIMEOUT_MS) {
    if (PMS.available() > 0) {
      uint8_t incomingByte = (uint8_t)PMS.read();
      anyByteSeen = true;

      if (index == 0) {
        if (incomingByte == PMS_START_BYTE_1) pmsBuffer[index++] = incomingByte;
      } else if (index == 1) {
        if (incomingByte == PMS_START_BYTE_2) pmsBuffer[index++] = incomingByte;
        else index = 0;
      } else {
        if (index < PMS_PACKET_SIZE) pmsBuffer[index++] = incomingByte;
        if (index >= PMS_PACKET_SIZE) break;
      }
    }
  }

  if (!anyByteSeen)          { pmsStatus = PMS_STATUS_NOT_DETECTED;   return; }
  if (index < PMS_PACKET_SIZE) { pmsStatus = PMS_STATUS_WAITING;        return; }
  if (pmsBuffer[0] != PMS_START_BYTE_1 || pmsBuffer[1] != PMS_START_BYTE_2) {
    pmsStatus = PMS_STATUS_INVALID_HEADER; return;
  }

  uint16_t calculatedSum = 0;
  for (uint8_t i = 0; i < PMS_PACKET_SIZE - 2; i++) calculatedSum += pmsBuffer[i];
  uint16_t receivedChecksum = ((uint16_t)pmsBuffer[PMS_PACKET_SIZE - 2] << 8) | pmsBuffer[PMS_PACKET_SIZE - 1];
  if (calculatedSum != receivedChecksum) { pmsStatus = PMS_STATUS_CHECKSUM_ERROR; return; }

  pmsData.pm1_0     = ((uint16_t)pmsBuffer[10] << 8) | pmsBuffer[11];
  pmsData.pm2_5     = ((uint16_t)pmsBuffer[12] << 8) | pmsBuffer[13];
  pmsData.pm10      = ((uint16_t)pmsBuffer[14] << 8) | pmsBuffer[15];
  pmsData.count0_3  = ((uint16_t)pmsBuffer[16] << 8) | pmsBuffer[17];
  pmsData.count0_5  = ((uint16_t)pmsBuffer[18] << 8) | pmsBuffer[19];
  pmsData.count1_0  = ((uint16_t)pmsBuffer[20] << 8) | pmsBuffer[21];
  pmsData.count2_5  = ((uint16_t)pmsBuffer[22] << 8) | pmsBuffer[23];
  pmsData.count5_0  = ((uint16_t)pmsBuffer[24] << 8) | pmsBuffer[25];
  pmsData.count10_0 = ((uint16_t)pmsBuffer[26] << 8) | pmsBuffer[27];
  pmsStatus = PMS_STATUS_OK;
#endif
}

// ===========================================================================
// FUNCTION: calculateAQI()
// ===========================================================================

int calculateAQI(float pm25) {
  float concentration = floorf(pm25 * 10.0f) / 10.0f;
  if (concentration < 0.0f) concentration = 0.0f;
  if (concentration > PM25_BREAKPOINTS[6].concHigh) concentration = PM25_BREAKPOINTS[6].concHigh;

  for (uint8_t i = 0; i < 7; i++) {
    if (concentration >= PM25_BREAKPOINTS[i].concLow &&
        concentration <= PM25_BREAKPOINTS[i].concHigh) {
      const AQIBreakpoint &bp = PM25_BREAKPOINTS[i];
      float aqi = ((float)(bp.aqiHigh - bp.aqiLow) / (bp.concHigh - bp.concLow)) *
                  (concentration - bp.concLow) + (float)bp.aqiLow;
      return (int)roundf(aqi);
    }
  }
  return 500;
}

// ===========================================================================
// FUNCTION: getAQICategory()
// ===========================================================================

const char* getAQICategory(int aqi) {
  if (aqi <= 50)  return "Good";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 150) return "Unhealthy for Sensitive Groups";
  if (aqi <= 200) return "Unhealthy";
  if (aqi <= 300) return "Very Unhealthy";
  return "Hazardous";
}

// ===========================================================================
// FUNCTION: printReport()
// ===========================================================================

void printReport() {
  Serial.println(F("======================================================"));
  Serial.println(F("AirGuard Air Quality Monitoring System"));
  Serial.println(F("======================================================"));
  Serial.println();

  Serial.println(F("PMS5003"));
  Serial.println();

  switch (pmsStatus) {
    case PMS_STATUS_NOT_DETECTED:   Serial.println(F("PMS5003 Not Detected"));   break;
    case PMS_STATUS_INVALID_HEADER: Serial.println(F("PMS5003 Invalid Packet")); break;
    case PMS_STATUS_CHECKSUM_ERROR: Serial.println(F("PMS5003 Checksum Error")); break;
    case PMS_STATUS_WAITING:        Serial.println(F("Waiting for PMS5003...")); break;
    case PMS_STATUS_OK:                                                           break;
  }
  Serial.println();

  if (pmsStatus == PMS_STATUS_OK) {
    Serial.printf("%-20s : %u ug/m3\n", "PM1.0", pmsData.pm1_0);
    Serial.printf("%-20s : %u ug/m3\n", "PM2.5", pmsData.pm2_5);
    Serial.printf("%-20s : %u ug/m3\n", "PM10",  pmsData.pm10);
    Serial.println();
    Serial.println(F("Particle Count"));
    Serial.println();
    Serial.printf("%-20s : %u\n", ">0.3 um",  pmsData.count0_3);
    Serial.printf("%-20s : %u\n", ">0.5 um",  pmsData.count0_5);
    Serial.printf("%-20s : %u\n", ">1.0 um",  pmsData.count1_0);
    Serial.printf("%-20s : %u\n", ">2.5 um",  pmsData.count2_5);
    Serial.printf("%-20s : %u\n", ">5.0 um",  pmsData.count5_0);
    Serial.printf("%-20s : %u\n", ">10.0 um", pmsData.count10_0);
  } else {
    Serial.printf("%-20s : N/A\n", "PM1.0");
    Serial.printf("%-20s : N/A\n", "PM2.5");
    Serial.printf("%-20s : N/A\n", "PM10");
    Serial.println();
    Serial.println(F("Particle Count"));
    Serial.println();
    Serial.printf("%-20s : N/A\n", ">0.3 um");
    Serial.printf("%-20s : N/A\n", ">0.5 um");
    Serial.printf("%-20s : N/A\n", ">1.0 um");
    Serial.printf("%-20s : N/A\n", ">2.5 um");
    Serial.printf("%-20s : N/A\n", ">5.0 um");
    Serial.printf("%-20s : N/A\n", ">10.0 um");
  }
  Serial.println();

  Serial.println(F("Gas Sensors"));
  Serial.println();
  Serial.printf("%-20s : %d\n",        "MQ135 Raw ADC",    mq135RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MQ135 Rs",         mq135RsKOhm);
  Serial.printf("%-20s : %.2f\n",      "MQ135 Rs/R0",      mq135RsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",        "MQ136 Raw ADC",    mq136RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MQ136 Rs",         mq136RsKOhm);
  Serial.printf("%-20s : %.2f\n",      "MQ136 Rs/R0",      mq136RsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",        "MiCS RED Raw ADC", micsRedRawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS RED Rs",      micsRedRsKOhm);
  Serial.printf("%-20s : %.2f\n",      "MiCS RED Rs/R0",   micsRedRsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",        "MiCS NOX Raw ADC", micsNoxRawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS NOX Rs",      micsNoxRsKOhm);
  Serial.printf("%-20s : %.2f\n",      "MiCS NOX Rs/R0",   micsNoxRsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",        "MP135 Raw ADC",    mp135RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MP135 Rs",         mp135RsKOhm);
  Serial.printf("%-20s : %.2f\n",      "MP135 Rs/R0",      mp135RsRatio);
  Serial.println();

  Serial.println(F("Gas Concentration"));
  Serial.println();
  if (calibrationValid) {
    Serial.printf("%-20s : %.1f ppm\n",   "CO2",  estimatedCO2);
    Serial.printf("%-20s : %.1f ppm\n",   "CO",   estimatedCO);
    Serial.printf("%-20s : %.2f ppm\n",   "NO2",  estimatedNO2);
    Serial.printf("%-20s : %.1f index\n", "VOC",  estimatedVOC);
    Serial.printf("%-20s : %.2f ppm\n",   "NH3",  estimatedNH3);
    Serial.printf("%-20s : %.2f ppm\n",   "H2S",  estimatedH2S);
  } else {
    Serial.printf("%-20s : Sensor Error\n", "CO2");
    Serial.printf("%-20s : Sensor Error\n", "CO");
    Serial.printf("%-20s : Sensor Error\n", "NO2");
    Serial.printf("%-20s : Sensor Error\n", "VOC");
    Serial.printf("%-20s : Sensor Error\n", "NH3");
    Serial.printf("%-20s : Sensor Error\n", "H2S");
  }
  Serial.println();

  if (pmsStatus == PMS_STATUS_OK) {
    currentAQI         = calculateAQI((float)pmsData.pm2_5);
    currentAQICategory = getAQICategory(currentAQI);
  } else {
    currentAQI         = 0;
    currentAQICategory = "N/A";
  }

  Serial.println(F("Air Quality"));
  Serial.println();
  if (pmsStatus == PMS_STATUS_OK) {
    Serial.printf("%-20s : %d\n", "AQI",      currentAQI);
    Serial.printf("%-20s : %s\n", "Category", currentAQICategory);
  } else {
    Serial.printf("%-20s : N/A\n", "AQI");
    Serial.printf("%-20s : N/A\n", "Category");
  }
  Serial.println();

  // ---- WiFi + Fan Status (new addition) ----
  Serial.println(F("Network & Purifier"));
  Serial.println();
  Serial.printf("%-20s : %s\n", "WiFi",    wifiOk ? "Connected" : "Offline");
  if (wifiOk) {
    Serial.printf("%-20s : %s\n", "ESP32 IP", WiFi.localIP().toString().c_str());
  }
  Serial.printf("%-20s : %s\n", "Fan D25", fanOn ? "ON (Active)" : "OFF (Standby)");
  Serial.println();

  Serial.println(F("======================================================"));
  Serial.println();
}
