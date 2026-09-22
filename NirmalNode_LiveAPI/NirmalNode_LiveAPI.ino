/*
  ===========================================================================
  NirmalNode – Green IoT Air Quality & Adaptive Air Purification Node
  ---------------------------------------------------------------------------
  BOARD            : ESP32 / ESP32-S3 Dev Module
  BAUD RATE        : 115200
  FEATURES         :
    1. PMS5003 Dust Sensor (UART)
    2. Multi-Gas Sensors (MQ135, MQ136, MiCS-4514 RED/NOX, MP135)
    3. Dual Format Serial Output (Human Readable Text & JSON API Stream)
    4. Purifier Relay Control Pin (Pre-emptive Fan Control)
  ===========================================================================
*/

#include <Arduino.h>

// Pin Definitions
#define PMS_RX_PIN        16      // ESP32 RX <- PMS5003 TXD
#define PMS_TX_PIN        -1      // Unused

#define MICS_RED_PIN      4       // MiCS-4514 RED channel (ESP32-S3 default) / 34 (ESP32 DevKit)
#define MICS_NOX_PIN      5       // MiCS-4514 NOX channel
#define MQ135_PIN         6       // MQ135 Air Quality
#define MQ136_PIN         7       // MQ136 H2S
#define MP135_PIN         15      // MP135 VOC

#define RELAY_FAN_PIN     18      // Relay Control for Cyclone-HEPA Fan

// ADC Configuration
const uint8_t ADC_RESOLUTION_BITS = 12;

// PMS5003 Frame
const uint8_t PMS_FRAME_LEN = 32;
uint8_t pmsBuffer[PMS_FRAME_LEN];
uint8_t pmsIndex = 0;

struct PMSData {
  uint16_t pm1_0 = 0;
  uint16_t pm2_5 = 0;
  uint16_t pm10  = 0;
  uint16_t cnt0_3 = 0;
  uint16_t cnt0_5 = 0;
  uint16_t cnt1_0 = 0;
  uint16_t cnt2_5 = 0;
  bool connected = false;
} pmsData;

HardwareSerial pmsSerial(1);
unsigned long lastReportTime = 0;
const unsigned long REPORT_INTERVAL_MS = 2000;

bool jsonOutputMode = false; // Toggle with command 'JSON' or 'TEXT'
bool purifierRelayState = false;

void readPMS();
void printTextReport();
void printJsonReport();

void setup() {
  Serial.begin(115200);
  pmsSerial.begin(9600, SERIAL_8N1, PMS_RX_PIN, PMS_TX_PIN);

  analogReadResolution(ADC_RESOLUTION_BITS);
  pinMode(RELAY_FAN_PIN, OUTPUT);
  digitalWrite(RELAY_FAN_PIN, LOW); // Off by default

  Serial.println(F("\n[NirmalNode] Firmware Initialized. Ready for Live API Dashboard connection.\n"));
}

void loop() {
  readPMS();

  // Handle incoming Serial commands from Web App or Python Server
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "FAN_ON") {
      purifierRelayState = true;
      digitalWrite(RELAY_FAN_PIN, HIGH);
      Serial.println(F("{\"status\":\"PURIFIER_FAN_ON\"}"));
    } else if (cmd == "FAN_OFF") {
      purifierRelayState = false;
      digitalWrite(RELAY_FAN_PIN, LOW);
      Serial.println(F("{\"status\":\"PURIFIER_FAN_OFF\"}"));
    } else if (cmd == "MODE_JSON") {
      jsonOutputMode = true;
    } else if (cmd == "MODE_TEXT") {
      jsonOutputMode = false;
    }
  }

  // Periodic Telemetry Output
  if (millis() - lastReportTime >= REPORT_INTERVAL_MS) {
    lastReportTime = millis();
    if (jsonOutputMode) {
      printJsonReport();
    } else {
      printTextReport();
    }
  }
}

void readPMS() {
  while (pmsSerial.available() > 0) {
    uint8_t b = pmsSerial.read();
    if (pmsIndex == 0 && b != 0x42) continue;
    if (pmsIndex == 1 && b != 0x4D) { pmsIndex = 0; continue; }
    
    pmsBuffer[pmsIndex++] = b;
    if (pmsIndex >= PMS_FRAME_LEN) {
      uint16_t sum = 0;
      for (uint8_t i = 0; i < PMS_FRAME_LEN - 2; i++) sum += pmsBuffer[i];
      uint16_t rxSum = ((uint16_t)pmsBuffer[30] << 8) | pmsBuffer[31];
      
      if (sum == rxSum) {
        pmsData.pm1_0  = ((uint16_t)pmsBuffer[10] << 8) | pmsBuffer[11];
        pmsData.pm2_5  = ((uint16_t)pmsBuffer[12] << 8) | pmsBuffer[13];
        pmsData.pm10   = ((uint16_t)pmsBuffer[14] << 8) | pmsBuffer[15];
        pmsData.cnt0_3 = ((uint16_t)pmsBuffer[16] << 8) | pmsBuffer[17];
        pmsData.connected = true;
      }
      pmsIndex = 0;
    }
  }
}

void printTextReport() {
  int mq135 = analogRead(MQ135_PIN);
  int mq136 = analogRead(MQ136_PIN);
  int micsRed = analogRead(MICS_RED_PIN);
  int micsNox = analogRead(MICS_NOX_PIN);
  int mp135 = analogRead(MP135_PIN);

  Serial.println(F("=============================="));
  Serial.println(F("NirmalNode Sensor Report"));
  Serial.println(F("=============================="));
  Serial.println(F("PMS5003"));
  Serial.println(F("--------"));
  if (pmsData.connected) {
    Serial.print(F("PM1.0 : ")); Serial.print(pmsData.pm1_0); Serial.println(F(" ug/m3"));
    Serial.print(F("PM2.5 : ")); Serial.print(pmsData.pm2_5); Serial.println(F(" ug/m3"));
    Serial.print(F("PM10  : ")); Serial.print(pmsData.pm10);  Serial.println(F(" ug/m3"));
    Serial.print(F("P>0.3um : ")); Serial.println(pmsData.cnt0_3);
  } else {
    Serial.println(F("PMS5003 : Not Detected"));
  }
  Serial.println();
  Serial.println(F("MiCS4514"));
  Serial.println(F("---------"));
  Serial.print(F("RED ADC : ")); Serial.println(micsRed);
  Serial.print(F("NOX ADC : ")); Serial.println(micsNox);
  Serial.println();
  Serial.println(F("MQ135"));
  Serial.print(F("ADC : ")); Serial.println(mq135);
  Serial.println();
  Serial.println(F("MQ136"));
  Serial.print(F("ADC : ")); Serial.println(mq136);
  Serial.println();
  Serial.println(F("MP135"));
  Serial.print(F("ADC : ")); Serial.println(mp135);
  Serial.println(F("=============================="));
  Serial.println();
}

void printJsonReport() {
  int mq135 = analogRead(MQ135_PIN);
  int mq136 = analogRead(MQ136_PIN);
  int micsRed = analogRead(MICS_RED_PIN);
  int micsNox = analogRead(MICS_NOX_PIN);
  int mp135 = analogRead(MP135_PIN);

  Serial.print(F("{\"pm1_0\":")); Serial.print(pmsData.pm1_0);
  Serial.print(F(",\"pm2_5\":")); Serial.print(pmsData.pm2_5);
  Serial.print(F(",\"pm10\":")); Serial.print(pmsData.pm10);
  Serial.print(F(",\"cnt0_3\":")); Serial.print(pmsData.cnt0_3);
  Serial.print(F(",\"mq135_adc\":")); Serial.print(mq135);
  Serial.print(F(",\"mq136_adc\":")); Serial.print(mq136);
  Serial.print(F(",\"mics_red_adc\":")); Serial.print(micsRed);
  Serial.print(F(",\"mics_nox_adc\":")); Serial.print(micsNox);
  Serial.print(F(",\"mp135_adc\":")); Serial.print(mp135);
  Serial.print(F(",\"fan_status\":")); Serial.print(purifierRelayState ? 1 : 0);
  Serial.println(F("}"));
}
