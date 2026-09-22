/*
  ===========================================================================
  AirGuard – Air Quality Monitoring System (Calibrated Estimation Build)
  ---------------------------------------------------------------------------
  BOARD            : ESP32 DevKit V1 (ESP-WROOM-32, 30-pin)
  CORE             : ESP32 Arduino Core 3.x

  SENSORS
    PMS5003    (UART2)  - Particulate Matter + Particle Counts (ACTUAL values)
    MQ135      (GPIO32) - Raw ADC + estimated CO2 / NH3 (ppm)
    MQ136      (GPIO33) - Raw ADC + estimated H2S (ppm)
    MiCS-4514 RED (GPIO34) - Raw ADC + estimated CO (ppm)
    MiCS-4514 NOX (GPIO35) - Raw ADC + estimated NO2 (ppm)
    MP135      (GPIO36 / VP) - Raw ADC + estimated generic VOC index

  ===========================================================================
  IMPORTANT ENGINEERING NOTICE — READ BEFORE TRUSTING ANY PPM VALUE
  ---------------------------------------------------------------------------
  MQ135 / MQ136 / MP135 / MiCS-4514 are resistive gas sensors. They do NOT
  output ppm directly. This firmware converts raw ADC -> voltage -> sensor
  resistance (Rs) -> Rs/R0 ratio -> ppm, using published datasheet-derived
  curve-fit coefficients (see GAS CURVE COEFFICIENTS section below).

  This produces an ESTIMATE, not a laboratory-grade measurement, because:
    1. R0 is determined here from a short power-on calibration in ambient
       room air (assumed clean), not a certified zero-gas reference chamber.
    2. The load resistor (RL) values below are typical/assumed. If your
       specific breakout board uses a different RL (many have a trimpot),
       you MUST update the *_RL_KOHM constants to match your hardware.
    3. Curve coefficients (a, b) for MQ135 CO2/NH3 come from widely-cited
       datasheet curve regressions; published values vary between sources
       by up to ~15-20%. MQ136, MP135 and MiCS-4514 coefficients here are
       rougher approximations since standardized public curve-fit data is
       far less consistent for these parts. Treat MP135 output as a
       relative index rather than a defensible ppm figure.
    4. Temperature/humidity compensation below uses FIXED ASSUMED values
       (see ASSUMED_TEMPERATURE_C / ASSUMED_HUMIDITY_PERCENT) because no
       physical temperature/humidity sensor is wired in this build. Real
       compensation requires a live DHT22/SHT31/BME280 reading — wiring
       one in is a straightforward future upgrade (see notes at bottom).

  All ppm figures below are printed with an explicit "(EST)" tag and should
  be presented as estimates in any report, paper, or demo — not as
  certified/reference-grade concentrations.
  ===========================================================================

  HARDWARE SAFETY WARNING — READ BEFORE POWERING ON
  ---------------------------------------------------------------------------
  These gas sensor modules run their heater/divider circuit at 5V (VIN).
  Their AO output can swing close to 5V under high gas concentration,
  which EXCEEDS the ESP32's 3.3V-max ADC input rating and can damage the
  GPIO pin permanently. If your AO lines are wired straight into GPIO32/
  33/34/35/36 with no protection, add a resistive voltage divider on each
  AO line before the ESP32 pin (e.g. 10k from AO to GPIO, 20k from GPIO to
  GND, giving a divider ratio of 0.667). Once added, update
  VOLTAGE_DIVIDER_RATIO below to match your resistor values so the Rs
  calculation can correctly recover the true sensor-side voltage. The
  default below (1.0) assumes NO divider is present, matching the wiring
  as originally specified — this is functional but carries real risk of
  ADC pin damage at high gas concentrations. Add the divider before
  extended/unattended operation.
  ===========================================================================
*/

#include <Arduino.h>
#include <math.h>

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

// Supply voltage actually driving the sensor's internal Rs/RL divider (VIN = 5V)
const float SENSOR_SUPPLY_VOLTAGE = 5.0f;

// Voltage divider ratio between sensor AO output and the ESP32 ADC pin.
// 1.0 = no external divider present (see HARDWARE SAFETY WARNING above).
// If you add a divider, set this to Vadc / Vsensor at the same operating point,
// e.g. 10k/20k divider -> ratio = 20 / (10 + 20) = 0.667
const float VOLTAGE_DIVIDER_RATIO = 1.0f;

// Load resistor values (kOhm). MUST match your physical module's RL/trimpot.
// Values below are commonly used defaults for hobbyist breakout boards.
const float MQ135_RL_KOHM     = 20.0f;
const float MQ136_RL_KOHM     = 20.0f;
const float MICS_RED_RL_KOHM  = 10.0f;
const float MICS_NOX_RL_KOHM  = 10.0f;
const float MP135_RL_KOHM     = 20.0f;

// ===========================================================================
// SECTION: Gas Curve Coefficients (ppm = a * (Rs/R0)^b)
// ===========================================================================
// MQ135 CO2/NH3 coefficients are widely-cited datasheet curve regressions
// (Gironi 2014 derivation for CO2; equivalent regression form for NH3).
// MQ136 / MiCS-4514 / MP135 coefficients are coarser approximations —
// see the engineering notice at the top of this file.

const float MQ135_CO2_CURVE_A = 116.6020682f;
const float MQ135_CO2_CURVE_B = -2.769034857f;

const float MQ135_NH3_CURVE_A = 102.694f;
const float MQ135_NH3_CURVE_B = -2.48818f;

const float MQ136_H2S_CURVE_A = 40.0f;   // Approximate — verify against your datasheet
const float MQ136_H2S_CURVE_B = -1.7f;   // Approximate — verify against your datasheet

const float MICS_RED_CO_CURVE_A = 4.4f;  // Approximate — verify against SGX datasheet
const float MICS_RED_CO_CURVE_B = -1.4f; // Approximate — verify against SGX datasheet

const float MICS_NOX_NO2_CURVE_A = 0.85f; // Approximate — verify against SGX datasheet
const float MICS_NOX_NO2_CURVE_B = 1.3f;  // Approximate — verify against SGX datasheet

const float MP135_VOC_CURVE_A = 5.0f;    // Very low confidence — treat as relative index
const float MP135_VOC_CURVE_B = -1.2f;   // Very low confidence — treat as relative index

// ===========================================================================
// SECTION: Temperature / Humidity Compensation (fixed assumed values)
// ===========================================================================
// No physical T/H sensor is wired in this build. Replace readAmbientTemp()
// and readAmbientHumidity() with live DHT22/SHT31/BME280 readings when one
// is added — the compensation formula below already expects live inputs.

const float ASSUMED_TEMPERATURE_C    = 25.0f; // Fixed default, no live sensor
const float ASSUMED_HUMIDITY_PERCENT = 65.0f; // Fixed default, no live sensor

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

const uint16_t CALIBRATION_SAMPLE_COUNT     = 50;   // Samples averaged for R0
const unsigned long CALIBRATION_INTERVAL_MS = 100;  // Delay between samples (setup only)
const unsigned long LOOP_DELAY_MS           = 2000; // Main loop cadence

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

// Baseline sensor resistance in clean air, determined at startup
float mq135R0     = 0.0f;
float mq136R0     = 0.0f;
float micsRedR0   = 0.0f;
float micsNoxR0   = 0.0f;
float mp135R0     = 0.0f;
bool  calibrationValid = false;

// Live estimated gas concentrations (ppm), populated each report cycle
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

// ===========================================================================
// FUNCTION PROTOTYPES
// ===========================================================================

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

// ===========================================================================
// SETUP
// ===========================================================================

void setup() {
  Serial.begin(115200);

  // ---- PMS5003 UART2 Initialization ----
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
  Serial.println(F("AirGuard system initializing..."));
  Serial.println(F("Gas sensors require a warmed-up, stable-air calibration"));
  Serial.println(F("period. Keep the device in clean, still air during this"));
  Serial.println(F("startup routine. Do not breathe near the sensors."));
  Serial.println(F("======================================================"));

  calibrateSensors();
}

// ===========================================================================
// LOOP
// ===========================================================================

void loop() {
  readPMS5003();
  readGasSensors();
  printReport();

  delay(LOOP_DELAY_MS); // Single delay() call in the entire program
}

// ===========================================================================
// FUNCTION: calibrateSensors()
// Performs a short power-on clean-air calibration to establish each gas
// sensor's baseline resistance (R0). Runs once in setup(). This is NOT a
// substitute for a proper certified-zero-gas calibration, but it gives a
// working baseline for relative ppm estimation.
// ===========================================================================

void calibrateSensors() {
  float mq135Sum   = 0.0f;
  float mq136Sum   = 0.0f;
  float micsRedSum = 0.0f;
  float micsNoxSum = 0.0f;
  float mp135Sum   = 0.0f;

  Serial.println(F("Calibrating baseline (R0) in current ambient air..."));

  for (uint16_t sample = 0; sample < CALIBRATION_SAMPLE_COUNT; sample++) {
    mq135Sum   += calculateRs(analogRead(MQ135_PIN),    MQ135_RL_KOHM);
    mq136Sum   += calculateRs(analogRead(MQ136_PIN),    MQ136_RL_KOHM);
    micsRedSum += calculateRs(analogRead(MICS_RED_PIN), MICS_RED_RL_KOHM);
    micsNoxSum += calculateRs(analogRead(MICS_NOX_PIN), MICS_NOX_RL_KOHM);
    mp135Sum   += calculateRs(analogRead(MP135_PIN),    MP135_RL_KOHM);

    delay(CALIBRATION_INTERVAL_MS); // Setup-only delay, not the main-loop delay
  }

  mq135R0   = mq135Sum   / (float)CALIBRATION_SAMPLE_COUNT;
  mq136R0   = mq136Sum   / (float)CALIBRATION_SAMPLE_COUNT;
  micsRedR0 = micsRedSum / (float)CALIBRATION_SAMPLE_COUNT;
  micsNoxR0 = micsNoxSum / (float)CALIBRATION_SAMPLE_COUNT;
  mp135R0   = mp135Sum   / (float)CALIBRATION_SAMPLE_COUNT;

  // Guard against a degenerate zero baseline (e.g. sensor disconnected)
  calibrationValid = (mq135R0 > 0.0f) && (mq136R0 > 0.0f) &&
                      (micsRedR0 > 0.0f) && (micsNoxR0 > 0.0f) && (mp135R0 > 0.0f);

  Serial.println(F("Calibration complete. Baseline R0 values (assumed clean air):"));
  Serial.printf("%-20s : %.2f kOhm\n", "MQ135 R0",     mq135R0);
  Serial.printf("%-20s : %.2f kOhm\n", "MQ136 R0",     mq136R0);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS RED R0",  micsRedR0);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS NOX R0",  micsNoxR0);
  Serial.printf("%-20s : %.2f kOhm\n", "MP135 R0",     mp135R0);

  if (!calibrationValid) {
    Serial.println(F("WARNING: One or more sensors returned an invalid baseline."));
    Serial.println(F("Check wiring. PPM estimates will be unreliable until fixed."));
  }
  Serial.println(F("======================================================"));
  Serial.println();
}

// ===========================================================================
// FUNCTION: calculateRs()
// Converts a raw ADC reading into sensor resistance (Rs, in kOhm) using the
// standard MQ-series voltage-divider relationship:
//   Rs = RL * (Vcc - Vsensor) / Vsensor
// Vsensor is recovered from the measured ADC voltage using the configured
// external voltage divider ratio (1.0 if no divider is present).
// ===========================================================================

float calculateRs(int adcRaw, float rlKOhm) {
  float adcVoltage = (adcRaw * ADC_REF_VOLTAGE) / (float)ADC_MAX_VALUE;

  // Recover the true sensor-side voltage if an external divider is present
  float sensorVoltage = adcVoltage / VOLTAGE_DIVIDER_RATIO;

  // Prevent division by zero / unrealistic values at the low end
  if (sensorVoltage < 0.01f) {
    sensorVoltage = 0.01f;
  }
  // Clamp to supply voltage ceiling to avoid negative Rs from ADC noise
  if (sensorVoltage > SENSOR_SUPPLY_VOLTAGE) {
    sensorVoltage = SENSOR_SUPPLY_VOLTAGE;
  }

  float rs = ((SENSOR_SUPPLY_VOLTAGE - sensorVoltage) / sensorVoltage) * rlKOhm;

  if (rs < 0.0f) {
    rs = 0.0f;
  }

  return rs;
}

// ===========================================================================
// FUNCTION: estimatePPM()
// Applies the published power-curve model ppm = a * (Rs/R0)^b to a given
// resistance ratio.
// ===========================================================================

float estimatePPM(float rsRatio, float curveA, float curveB) {
  if (rsRatio <= 0.0f) {
    return 0.0f;
  }
  return curveA * powf(rsRatio, curveB);
}

// ===========================================================================
// FUNCTION: readAmbientTemperature() / readAmbientHumidity()
// No physical temperature/humidity sensor is wired in this build, so these
// return fixed assumed ambient values. Replace the body of these two
// functions with live DHT22/SHT31/BME280 reads to enable true compensation;
// every other function already consumes their return values directly.
// ===========================================================================

float readAmbientTemperature() {
  return ASSUMED_TEMPERATURE_C;
}

float readAmbientHumidity() {
  return ASSUMED_HUMIDITY_PERCENT;
}

// ===========================================================================
// FUNCTION: applyTempHumidityCorrection()
// Applies a datasheet-derived temperature/humidity correction factor to a
// measured Rs/R0 ratio, referenced to the MQ135 datasheet's standard
// calibration point (20 degC, 65% RH). The same correction is applied
// across all resistive sensors here as a practical approximation, since
// dedicated per-gas correction curves are not consistently published.
// ===========================================================================

float applyTempHumidityCorrection(float rsRatio, float temperatureC, float humidityPercent) {
  float correctionFactor = (0.00035f * temperatureC * temperatureC)
                            - (0.02718f * temperatureC)
                            + 1.39538f
                            - ((humidityPercent - 33.0f) * 0.0018f);

  if (correctionFactor < 0.01f) {
    correctionFactor = 0.01f; // Guard against non-physical correction
  }

  return rsRatio / correctionFactor;
}

// ===========================================================================
// FUNCTION: readGasSensors()
// Reads raw ADC values, computes Rs/R0 ratios, applies temperature/humidity
// correction, and estimates ppm concentrations for every gas channel.
// ===========================================================================

void readGasSensors() {
  float temperatureC    = readAmbientTemperature();
  float humidityPercent = readAmbientHumidity();

  // ---- MQ135: CO2 (primary) and NH3 (secondary curve) ----
  mq135RawADC  = analogRead(MQ135_PIN);
  mq135RsKOhm  = calculateRs(mq135RawADC, MQ135_RL_KOHM);
  mq135RsRatio = calibrationValid ? applyTempHumidityCorrection(mq135RsKOhm / mq135R0, temperatureC, humidityPercent) : 0.0f;
  estimatedCO2 = calibrationValid ? estimatePPM(mq135RsRatio, MQ135_CO2_CURVE_A, MQ135_CO2_CURVE_B) : 0.0f;
  estimatedNH3 = calibrationValid ? estimatePPM(mq135RsRatio, MQ135_NH3_CURVE_A, MQ135_NH3_CURVE_B) : 0.0f;

  // ---- MQ136: H2S ----
  mq136RawADC  = analogRead(MQ136_PIN);
  mq136RsKOhm  = calculateRs(mq136RawADC, MQ136_RL_KOHM);
  mq136RsRatio = calibrationValid ? applyTempHumidityCorrection(mq136RsKOhm / mq136R0, temperatureC, humidityPercent) : 0.0f;
  estimatedH2S = calibrationValid ? estimatePPM(mq136RsRatio, MQ136_H2S_CURVE_A, MQ136_H2S_CURVE_B) : 0.0f;

  // ---- MiCS-4514 RED: CO ----
  micsRedRawADC  = analogRead(MICS_RED_PIN);
  micsRedRsKOhm  = calculateRs(micsRedRawADC, MICS_RED_RL_KOHM);
  micsRedRsRatio = calibrationValid ? (micsRedRsKOhm / micsRedR0) : 0.0f;
  estimatedCO    = calibrationValid ? estimatePPM(micsRedRsRatio, MICS_RED_CO_CURVE_A, MICS_RED_CO_CURVE_B) : 0.0f;

  // ---- MiCS-4514 NOX: NO2 ----
  micsNoxRawADC  = analogRead(MICS_NOX_PIN);
  micsNoxRsKOhm  = calculateRs(micsNoxRawADC, MICS_NOX_RL_KOHM);
  micsNoxRsRatio = calibrationValid ? (micsNoxRsKOhm / micsNoxR0) : 0.0f;
  estimatedNO2   = calibrationValid ? estimatePPM(micsNoxRsRatio, MICS_NOX_NO2_CURVE_A, MICS_NOX_NO2_CURVE_B) : 0.0f;

  // ---- MP135: generic VOC relative index (lowest confidence) ----
  mp135RawADC  = analogRead(MP135_PIN);
  mp135RsKOhm  = calculateRs(mp135RawADC, MP135_RL_KOHM);
  mp135RsRatio = calibrationValid ? (mp135RsKOhm / mp135R0) : 0.0f;
  estimatedVOC = calibrationValid ? estimatePPM(mp135RsRatio, MP135_VOC_CURVE_A, MP135_VOC_CURVE_B) : 0.0f;
}

// ===========================================================================
// FUNCTION: readPMS5003()
// Reads and validates one complete PMS5003 32-byte packet within a bounded
// timeout window. Sets pmsStatus and, on success, populates pmsData.
// ===========================================================================

void readPMS5003() {
  unsigned long startTime   = millis();
  bool          anyByteSeen = false;
  uint8_t       index       = 0;

  while ((millis() - startTime) < PMS_READ_TIMEOUT_MS) {
    if (PMS.available() > 0) {
      uint8_t incomingByte = (uint8_t)PMS.read();
      anyByteSeen = true;

      if (index == 0) {
        if (incomingByte == PMS_START_BYTE_1) {
          pmsBuffer[index++] = incomingByte;
        }
      } else if (index == 1) {
        if (incomingByte == PMS_START_BYTE_2) {
          pmsBuffer[index++] = incomingByte;
        } else {
          index = 0;
        }
      } else {
        if (index < PMS_PACKET_SIZE) {
          pmsBuffer[index++] = incomingByte;
        }
        if (index >= PMS_PACKET_SIZE) {
          break;
        }
      }
    }
  }

  if (!anyByteSeen) {
    pmsStatus = PMS_STATUS_NOT_DETECTED;
    return;
  }

  if (index < PMS_PACKET_SIZE) {
    pmsStatus = PMS_STATUS_WAITING;
    return;
  }

  if (pmsBuffer[0] != PMS_START_BYTE_1 || pmsBuffer[1] != PMS_START_BYTE_2) {
    pmsStatus = PMS_STATUS_INVALID_HEADER;
    return;
  }

  uint16_t calculatedSum = 0;
  for (uint8_t i = 0; i < PMS_PACKET_SIZE - 2; i++) {
    calculatedSum += pmsBuffer[i];
  }
  uint16_t receivedChecksum =
      ((uint16_t)pmsBuffer[PMS_PACKET_SIZE - 2] << 8) | pmsBuffer[PMS_PACKET_SIZE - 1];

  if (calculatedSum != receivedChecksum) {
    pmsStatus = PMS_STATUS_CHECKSUM_ERROR;
    return;
  }

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
}

// ===========================================================================
// FUNCTION: calculateAQI()
// Computes the official US EPA Air Quality Index from a PM2.5 concentration
// (µg/m3) using linear interpolation across the standard breakpoint table.
// ===========================================================================

int calculateAQI(float pm25) {
  float concentration = floorf(pm25 * 10.0f) / 10.0f;

  if (concentration < 0.0f) {
    concentration = 0.0f;
  }
  if (concentration > PM25_BREAKPOINTS[6].concHigh) {
    concentration = PM25_BREAKPOINTS[6].concHigh;
  }

  for (uint8_t i = 0; i < 7; i++) {
    if (concentration >= PM25_BREAKPOINTS[i].concLow &&
        concentration <= PM25_BREAKPOINTS[i].concHigh) {
      const AQIBreakpoint &bp = PM25_BREAKPOINTS[i];

      float aqi = ((float)(bp.aqiHigh - bp.aqiLow) / (bp.concHigh - bp.concLow)) *
                      (concentration - bp.concLow) +
                  (float)bp.aqiLow;

      return (int)roundf(aqi);
    }
  }

  return 500;
}

// ===========================================================================
// FUNCTION: getAQICategory()
// Maps a calculated AQI value to its official US EPA category name.
// ===========================================================================

const char* getAQICategory(int aqi) {
  if (aqi <= 50) {
    return "Good";
  } else if (aqi <= 100) {
    return "Moderate";
  } else if (aqi <= 150) {
    return "Unhealthy for Sensitive Groups";
  } else if (aqi <= 200) {
    return "Unhealthy";
  } else if (aqi <= 300) {
    return "Very Unhealthy";
  } else {
    return "Hazardous";
  }
}

// ===========================================================================
// FUNCTION: printReport()
// Prints the complete, formatted sensor report to the Serial Monitor.
// ===========================================================================

void printReport() {
  Serial.println(F("======================================================"));
  Serial.println(F("AirGuard Air Quality Monitoring System"));
  Serial.println(F("======================================================"));
  Serial.println();

  // ---- PMS5003 Section (actual values, no calibration needed) ----
  Serial.println(F("PMS5003"));
  Serial.println();

  switch (pmsStatus) {
    case PMS_STATUS_NOT_DETECTED:   Serial.println(F("PMS5003 Not Detected"));   break;
    case PMS_STATUS_INVALID_HEADER: Serial.println(F("PMS5003 Invalid Packet")); break;
    case PMS_STATUS_CHECKSUM_ERROR: Serial.println(F("PMS5003 Checksum Error")); break;
    case PMS_STATUS_WAITING:        Serial.println(F("Waiting for PMS5003...")); break;
    case PMS_STATUS_OK:                                                          break;
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

  // ---- Gas Sensors Section: raw ADC + resistance diagnostics ----
  Serial.println(F("Gas Sensors (Raw + Diagnostics)"));
  Serial.println();
  Serial.printf("%-20s : %d\n",      "MQ135 Raw ADC",    mq135RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MQ135 Rs",       mq135RsKOhm);
  Serial.printf("%-20s : %.2f\n",    "MQ135 Rs/R0",      mq135RsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",      "MQ136 Raw ADC",    mq136RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MQ136 Rs",       mq136RsKOhm);
  Serial.printf("%-20s : %.2f\n",    "MQ136 Rs/R0",      mq136RsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",      "MiCS RED Raw ADC", micsRedRawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS RED Rs",    micsRedRsKOhm);
  Serial.printf("%-20s : %.2f\n",    "MiCS RED Rs/R0",   micsRedRsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",      "MiCS NOX Raw ADC", micsNoxRawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MiCS NOX Rs",    micsNoxRsKOhm);
  Serial.printf("%-20s : %.2f\n",    "MiCS NOX Rs/R0",   micsNoxRsRatio);
  Serial.println();
  Serial.printf("%-20s : %d\n",      "MP135 Raw ADC",    mp135RawADC);
  Serial.printf("%-20s : %.2f kOhm\n", "MP135 Rs",       mp135RsKOhm);
  Serial.printf("%-20s : %.2f\n",    "MP135 Rs/R0",      mp135RsRatio);
  Serial.println();

  // ---- Estimated Values Section ----
  Serial.println(F("Estimated Values (EST - not lab-calibrated)"));
  Serial.println();
  if (calibrationValid) {
    Serial.printf("%-20s : %.1f ppm (EST)\n", "CO2",  estimatedCO2);
    Serial.printf("%-20s : %.1f ppm (EST)\n", "CO",   estimatedCO);
    Serial.printf("%-20s : %.2f ppm (EST)\n", "NO2",  estimatedNO2);
    Serial.printf("%-20s : %.1f index (EST)\n", "VOC", estimatedVOC);
    Serial.printf("%-20s : %.2f ppm (EST)\n", "NH3",  estimatedNH3);
    Serial.printf("%-20s : %.2f ppm (EST)\n", "H2S",  estimatedH2S);
  } else {
    Serial.printf("%-20s : Calibration invalid\n", "CO2");
    Serial.printf("%-20s : Calibration invalid\n", "CO");
    Serial.printf("%-20s : Calibration invalid\n", "NO2");
    Serial.printf("%-20s : Calibration invalid\n", "VOC");
    Serial.printf("%-20s : Calibration invalid\n", "NH3");
    Serial.printf("%-20s : Calibration invalid\n", "H2S");
  }
  Serial.println();

  // ---- Air Quality Section (based on actual PMS2.5 data, EPA formula) ----
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
    Serial.printf("%-20s : %d\n", "AQI", currentAQI);
  } else {
    Serial.printf("%-20s : N/A\n", "AQI");
  }
  Serial.printf("%-20s : %s\n", "Category", currentAQICategory);
  Serial.println();

  Serial.println(F("======================================================"));
  Serial.println();
}
