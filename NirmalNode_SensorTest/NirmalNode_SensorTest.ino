/*
  ===========================================================================
  NirmalNode – Green IoT and AI Assisted Local Air Purification
              and Pollution Prediction System
  ---------------------------------------------------------------------------
  PHASE            : Sensor Testing Only
  CONTROLLER       : ESP32-S3 Dev Module
  POWER SUPPLY     : 5V DC Bench Supply (APS3005D)

  SENSORS
    1. PMS5003    (UART)  - Particulate Matter (PM1.0 / PM2.5 / PM10 + counts)
    2. MiCS-4514  (ADC)   - RED (Oxidizing gases) + NOX channels
    3. MQ135      (ADC)   - Air Quality / CO2-equivalent gases
    4. MQ136      (ADC)   - H2S / Sulphur compounds
    5. MP135      (ADC)   - Analog gas channel

  LIBRARIES USED   : None external. Only built-in ESP32 Arduino Core
                      (HardwareSerial, analogRead API).

  NOTES
    - No WiFi / MQTT / ThingSpeak / Blynk / OLED / LCD / SD / AI in this phase.
    - Code is modular so these can be added later without restructuring.
    - No delay() is used anywhere except the non-blocking millis() based
      3-second report scheduler (which itself does not use delay()).
  ===========================================================================
*/

#include <Arduino.h>

// ===========================================================================
// SECTION: Pin Definitions
// ===========================================================================

// ---- PMS5003 (Dust Sensor) — UART1 ----
#define PMS_RX_PIN        16      // ESP32 RX  <- PMS5003 TXD
#define PMS_TX_PIN        -1      // Not connected (PMS RXD unused)
#define PMS_BAUD_RATE     9600

// ---- MiCS-4514 (Gas Sensor) — Analog ----
#define MICS_RED_PIN      4       // RED (oxidizing) channel
#define MICS_NOX_PIN      5       // NOX channel

// ---- MQ135 (Air Quality) — Analog ----
#define MQ135_PIN         6

// ---- MQ136 (H2S / Sulphur) — Analog ----
#define MQ136_PIN         7

// ---- MP135 (Gas Sensor) — Analog ----
#define MP135_PIN         15

// ===========================================================================
// SECTION: ADC Configuration Constants
// ===========================================================================

const uint8_t  ADC_RESOLUTION_BITS = 12;         // ESP32-S3 supports up to 12-bit
const int      ADC_MAX_VALUE       = 4095;       // 2^12 - 1
const float    ADC_REF_VOLTAGE     = 3.3f;       // Reference voltage after attenuation
const adc_attenuation_t ADC_ATTEN  = ADC_11db;    // ~0 - 3.3V input range

// ===========================================================================
// SECTION: PMS5003 Protocol Constants
// ===========================================================================

const uint8_t  PMS_FRAME_LEN        = 32;    // Total bytes in one PMS5003 frame
const uint8_t  PMS_START_BYTE_1     = 0x42;
const uint8_t  PMS_START_BYTE_2     = 0x4D;
const unsigned long PMS_TIMEOUT_MS  = 5000;  // No valid frame -> "Not Detected"

// ===========================================================================
// SECTION: Timing Constants
// ===========================================================================

const unsigned long REPORT_INTERVAL_MS = 3000; // Serial report every 3 seconds

// ===========================================================================
// SECTION: Global Objects
// ===========================================================================

HardwareSerial pmsSerial(1);   // UART1 used exclusively for PMS5003

// ===========================================================================
// SECTION: Data Structures
// ===========================================================================

struct PMSData {
  uint16_t pm1_0   = 0;   // PM1.0  (atmospheric, ug/m3)
  uint16_t pm2_5   = 0;   // PM2.5  (atmospheric, ug/m3)
  uint16_t pm10    = 0;   // PM10   (atmospheric, ug/m3)

  uint16_t cnt0_3  = 0;   // Particles > 0.3um / 0.1L air
  uint16_t cnt0_5  = 0;   // Particles > 0.5um / 0.1L air
  uint16_t cnt1_0  = 0;   // Particles > 1.0um / 0.1L air
  uint16_t cnt2_5  = 0;   // Particles > 2.5um / 0.1L air
  uint16_t cnt5_0  = 0;   // Particles > 5.0um / 0.1L air
  uint16_t cnt10_0 = 0;   // Particles > 10.0um / 0.1L air

  bool connected        = false;
  unsigned long lastValidTime = 0;
};

struct GasChannel {
  int   adcValue = 0;
  float voltage  = 0.0f;
  bool  error    = false;
};

// Global sensor data instances
PMSData     pmsData;
GasChannel  micsRed;
GasChannel  micsNox;
GasChannel  mq135;
GasChannel  mq136;
GasChannel  mp135;

// Report scheduling
unsigned long lastReportTime = 0;

// PMS byte-parser state
uint8_t pmsBuffer[PMS_FRAME_LEN];
uint8_t pmsIndex = 0;

// ===========================================================================
// FUNCTION PROTOTYPES
// ===========================================================================

void readPMS();
void readMiCS();
void readMQ135();
void readMQ136();
void readMP135();
void printReport();
float adcToVoltage(int adcValue);
int   readADCSafe(uint8_t pin, bool &errorFlag);
void  readGasChannel(uint8_t pin, GasChannel &channel);

// ===========================================================================
// SETUP
// ===========================================================================

void setup() {
  // ---- Debug / Report Serial ----
  Serial.begin(115200);
  while (!Serial) { ; }   // Wait for native USB CDC on ESP32-S3 (harmless on UART0)

  // ---- PMS5003 UART Initialization ----
  pmsSerial.begin(PMS_BAUD_RATE, SERIAL_8N1, PMS_RX_PIN, PMS_TX_PIN);

  // ---- ADC Global Resolution ----
  analogReadResolution(ADC_RESOLUTION_BITS);

  // ---- Per-Pin Attenuation (0 - ~3.3V full range) ----
  analogSetPinAttenuation(MICS_RED_PIN, ADC_ATTEN);
  analogSetPinAttenuation(MICS_NOX_PIN, ADC_ATTEN);
  analogSetPinAttenuation(MQ135_PIN,    ADC_ATTEN);
  analogSetPinAttenuation(MQ136_PIN,    ADC_ATTEN);
  analogSetPinAttenuation(MP135_PIN,    ADC_ATTEN);

  // pmsData.lastValidTime stays 0 so PMS is correctly reported
  // as "Not Detected" until the first valid frame arrives.

  Serial.println();
  Serial.println(F("NirmalNode Sensor Testing Phase Initialized."));
  Serial.println(F("Waiting for first report cycle..."));
  Serial.println();
}

// ===========================================================================
// LOOP
// ===========================================================================

void loop() {
  // Continuously service the PMS5003 UART buffer (non-blocking)
  readPMS();

  // Continuously sample analog gas sensors (cheap, non-blocking reads)
  readMiCS();
  readMQ135();
  readMQ136();
  readMP135();

  // Print consolidated report every REPORT_INTERVAL_MS using millis()
  unsigned long now = millis();
  if (now - lastReportTime >= REPORT_INTERVAL_MS) {
    lastReportTime = now;
    printReport();
  }
}

// ===========================================================================
// FUNCTION: readPMS()
// Reads and parses PMS5003 UART frames in a non-blocking byte-state-machine.
// Handles invalid packets (checksum mismatch) and disconnection timeout.
// ===========================================================================

void readPMS() {
  while (pmsSerial.available() > 0) {
    uint8_t incomingByte = (uint8_t)pmsSerial.read();

    if (pmsIndex == 0) {
      // Waiting for first start byte
      if (incomingByte == PMS_START_BYTE_1) {
        pmsBuffer[pmsIndex++] = incomingByte;
      }
      continue;
    }

    if (pmsIndex == 1) {
      // Waiting for second start byte
      if (incomingByte == PMS_START_BYTE_2) {
        pmsBuffer[pmsIndex++] = incomingByte;
      } else {
        pmsIndex = 0; // Resync: invalid header
      }
      continue;
    }

    // Collecting remaining frame bytes
    pmsBuffer[pmsIndex++] = incomingByte;

    if (pmsIndex >= PMS_FRAME_LEN) {
      pmsIndex = 0; // Reset for next frame

      // ---- Checksum Validation ----
      uint16_t calculatedSum = 0;
      for (uint8_t i = 0; i < PMS_FRAME_LEN - 2; i++) {
        calculatedSum += pmsBuffer[i];
      }
      uint16_t receivedChecksum =
          ((uint16_t)pmsBuffer[PMS_FRAME_LEN - 2] << 8) | pmsBuffer[PMS_FRAME_LEN - 1];

      if (calculatedSum == receivedChecksum) {
        // ---- Valid Frame: Parse Data (Atmospheric Environment values) ----
        pmsData.pm1_0   = ((uint16_t)pmsBuffer[10] << 8) | pmsBuffer[11];
        pmsData.pm2_5   = ((uint16_t)pmsBuffer[12] << 8) | pmsBuffer[13];
        pmsData.pm10    = ((uint16_t)pmsBuffer[14] << 8) | pmsBuffer[15];

        pmsData.cnt0_3  = ((uint16_t)pmsBuffer[16] << 8) | pmsBuffer[17];
        pmsData.cnt0_5  = ((uint16_t)pmsBuffer[18] << 8) | pmsBuffer[19];
        pmsData.cnt1_0  = ((uint16_t)pmsBuffer[20] << 8) | pmsBuffer[21];
        pmsData.cnt2_5  = ((uint16_t)pmsBuffer[22] << 8) | pmsBuffer[23];
        pmsData.cnt5_0  = ((uint16_t)pmsBuffer[24] << 8) | pmsBuffer[25];
        pmsData.cnt10_0 = ((uint16_t)pmsBuffer[26] << 8) | pmsBuffer[27];

        pmsData.connected     = true;
        pmsData.lastValidTime = millis();
      }
      // Invalid packet (checksum mismatch) -> silently discarded,
      // previous good values are retained until timeout occurs.
    }
  }

  // ---- Disconnection / Timeout Detection ----
  if (pmsData.connected && (millis() - pmsData.lastValidTime > PMS_TIMEOUT_MS)) {
    pmsData.connected = false;
  }
}

// ===========================================================================
// FUNCTION: adcToVoltage()
// Converts a raw ADC reading into an actual voltage value.
// ===========================================================================

float adcToVoltage(int adcValue) {
  return (adcValue * ADC_REF_VOLTAGE) / (float)ADC_MAX_VALUE;
}

// ===========================================================================
// FUNCTION: readADCSafe()
// Performs an analogRead() with basic error detection.
// ESP32 Arduino core returns a negative value if the ADC read fails
// (e.g. invalid channel / driver conflict).
// ===========================================================================

int readADCSafe(uint8_t pin, bool &errorFlag) {
  int rawValue = analogRead(pin);

  if (rawValue < 0) {
    errorFlag = true;
    return 0;
  }

  errorFlag = false;
  return rawValue;
}

// ===========================================================================
// FUNCTION: readGasChannel()
// Generic helper: reads one analog gas channel and converts to voltage.
// ===========================================================================

void readGasChannel(uint8_t pin, GasChannel &channel) {
  channel.adcValue = readADCSafe(pin, channel.error);
  channel.voltage  = channel.error ? 0.0f : adcToVoltage(channel.adcValue);
}

// ===========================================================================
// FUNCTION: readMiCS()
// Reads MiCS-4514 RED and NOX channels.
// ===========================================================================

void readMiCS() {
  readGasChannel(MICS_RED_PIN, micsRed);
  readGasChannel(MICS_NOX_PIN, micsNox);
}

// ===========================================================================
// FUNCTION: readMQ135()
// Reads MQ135 analog output.
// ===========================================================================

void readMQ135() {
  readGasChannel(MQ135_PIN, mq135);
}

// ===========================================================================
// FUNCTION: readMQ136()
// Reads MQ136 analog output.
// ===========================================================================

void readMQ136() {
  readGasChannel(MQ136_PIN, mq136);
}

// ===========================================================================
// FUNCTION: readMP135()
// Reads MP135 analog output.
// ===========================================================================

void readMP135() {
  readGasChannel(MP135_PIN, mp135);
}

// ===========================================================================
// FUNCTION: printReport()
// Prints a clean, formatted consolidated sensor report to Serial Monitor.
// ===========================================================================

void printReport() {
  Serial.println(F("=============================="));
  Serial.println(F("NirmalNode Sensor Report"));
  Serial.println(F("=============================="));

  // ---- PMS5003 ----
  Serial.println(F("PMS5003"));
  Serial.println(F("--------"));
  if (pmsData.connected) {
    Serial.print(F("PM1.0 : ")); Serial.print(pmsData.pm1_0); Serial.println(F(" ug/m3"));
    Serial.print(F("PM2.5 : ")); Serial.print(pmsData.pm2_5); Serial.println(F(" ug/m3"));
    Serial.print(F("PM10  : ")); Serial.print(pmsData.pm10);  Serial.println(F(" ug/m3"));
    Serial.print(F("P>0.3um : ")); Serial.println(pmsData.cnt0_3);
    Serial.print(F("P>0.5um : ")); Serial.println(pmsData.cnt0_5);
    Serial.print(F("P>1.0um : ")); Serial.println(pmsData.cnt1_0);
    Serial.print(F("P>2.5um : ")); Serial.println(pmsData.cnt2_5);
    Serial.print(F("P>5.0um : ")); Serial.println(pmsData.cnt5_0);
    Serial.print(F("P>10um  : ")); Serial.println(pmsData.cnt10_0);
  } else {
    Serial.println(F("PMS5003 : Not Detected"));
  }
  Serial.println();

  // ---- MiCS-4514 ----
  Serial.println(F("MiCS4514"));
  Serial.println(F("---------"));
  if (micsRed.error || micsNox.error) {
    Serial.println(F("Sensor Error"));
  } else {
    Serial.print(F("RED ADC : ")); Serial.println(micsRed.adcValue);
    Serial.print(F("RED Volt: ")); Serial.print(micsRed.voltage, 2); Serial.println(F(" V"));
    Serial.print(F("NOX ADC : ")); Serial.println(micsNox.adcValue);
    Serial.print(F("NOX Volt: ")); Serial.print(micsNox.voltage, 2); Serial.println(F(" V"));
  }
  Serial.println();

  // ---- MQ135 ----
  Serial.println(F("MQ135"));
  Serial.println(F("------"));
  if (mq135.error) {
    Serial.println(F("Sensor Error"));
  } else {
    Serial.print(F("ADC : ")); Serial.println(mq135.adcValue);
    Serial.print(F("Volt: ")); Serial.print(mq135.voltage, 2); Serial.println(F(" V"));
  }
  Serial.println();

  // ---- MQ136 ----
  Serial.println(F("MQ136"));
  Serial.println(F("------"));
  if (mq136.error) {
    Serial.println(F("Sensor Error"));
  } else {
    Serial.print(F("ADC : ")); Serial.println(mq136.adcValue);
    Serial.print(F("Volt: ")); Serial.print(mq136.voltage, 2); Serial.println(F(" V"));
  }
  Serial.println();

  // ---- MP135 ----
  Serial.println(F("MP135"));
  Serial.println(F("------"));
  if (mp135.error) {
    Serial.println(F("Sensor Error"));
  } else {
    Serial.print(F("ADC : ")); Serial.println(mp135.adcValue);
    Serial.print(F("Volt: ")); Serial.print(mp135.voltage, 2); Serial.println(F(" V"));
  }
  Serial.println();

  // ---- Timestamp ----
  Serial.print(F("Timestamp : "));
  Serial.print(millis() / 1000);
  Serial.println(F(" sec"));

  Serial.println(F("=============================="));
  Serial.println();
}

// ===========================================================================
// FUTURE EXPANSION HOOKS (Not active in this phase)
// ===========================================================================
// - connectWiFi()          -> Add WiFi.h based connectivity
// - sendToThingSpeak()     -> Push pmsData / gas values via HTTP
// - runInferenceModel()    -> Feed sensor values into TinyML model
// - controlRelay()         -> Drive fan/purifier relay based on AQI logic
// - updateOLED()           -> Mirror printReport() output to a display
// These can be added as new functions and called from loop() without
// modifying the existing sensor-reading logic above.
// ===========================================================================
