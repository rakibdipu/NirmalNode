/*
  ===========================================================================
  AirGuard – Air Quality Monitoring System
  ---------------------------------------------------------------------------
  BOARD            : ESP32 DevKit V1 (ESP-WROOM-32, 30-pin)
  CORE             : ESP32 Arduino Core 3.x

  SENSORS
    PMS5003    (UART2)  - Particulate Matter + Particle Counts
    MQ135      (GPIO32) - Raw ADC only (not calibrated)
    MQ136      (GPIO33) - Raw ADC only (not calibrated)
    MiCS-4514 RED (GPIO34) - Raw ADC only (not calibrated)
    MiCS-4514 NOX (GPIO35) - Raw ADC only (not calibrated)
    MP135      (GPIO36 / VP) - Raw ADC only (not calibrated)

  NOTES
    - No external libraries. Only built-in ESP32 Arduino Core APIs.
    - No String class usage; no dynamic memory allocation.
    - Exactly one delay(2000) call exists in the entire program (main loop).
    - AQI is computed from PM2.5 using the official US EPA breakpoint table.
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

const uint8_t ADC_RESOLUTION_BITS = 12;     // 0 - 4095
const adc_attenuation_t ADC_ATTEN = ADC_11db; // Full ~0 - 3.3V input range

// ===========================================================================
// SECTION: PMS5003 Protocol Constants
// ===========================================================================

const uint8_t PMS_PACKET_SIZE     = 32;
const uint8_t PMS_START_BYTE_1    = 0x42;
const uint8_t PMS_START_BYTE_2    = 0x4D;
const unsigned long PMS_READ_TIMEOUT_MS = 1500; // Max wait per read cycle

// ===========================================================================
// SECTION: Timing Constants
// ===========================================================================

const unsigned long LOOP_DELAY_MS = 2000; // Main loop cadence (single delay call)

// ===========================================================================
// SECTION: Global Objects
// ===========================================================================

HardwareSerial PMS(2); // UART2 dedicated to PMS5003

// ===========================================================================
// SECTION: Data Structures
// ===========================================================================

// PMS5003 read status codes
enum PMSStatus {
  PMS_STATUS_OK,
  PMS_STATUS_NOT_DETECTED,
  PMS_STATUS_INVALID_HEADER,
  PMS_STATUS_CHECKSUM_ERROR,
  PMS_STATUS_WAITING
};

struct PMSData {
  uint16_t pm1_0   = 0;
  uint16_t pm2_5   = 0;
  uint16_t pm10    = 0;

  uint16_t count0_3  = 0;
  uint16_t count0_5  = 0;
  uint16_t count1_0  = 0;
  uint16_t count2_5  = 0;
  uint16_t count5_0  = 0;
  uint16_t count10_0 = 0;
};

// AQI breakpoint entry (US EPA PM2.5 table)
struct AQIBreakpoint {
  float concLow;
  float concHigh;
  int   aqiLow;
  int   aqiHigh;
};

// US EPA PM2.5 24-hr breakpoint table
const AQIBreakpoint PM25_BREAKPOINTS[7] = {
  {  0.0f,  12.0f,   0,  50 },  // Good
  { 12.1f,  35.4f,  51, 100 },  // Moderate
  { 35.5f,  55.4f, 101, 150 },  // Unhealthy for Sensitive Groups
  { 55.5f, 150.4f, 151, 200 },  // Unhealthy
  {150.5f, 250.4f, 201, 300 },  // Very Unhealthy
  {250.5f, 350.4f, 301, 400 },  // Hazardous
  {350.5f, 500.4f, 401, 500 }   // Hazardous
};

// ===========================================================================
// SECTION: Global State
// ===========================================================================

uint8_t    pmsBuffer[PMS_PACKET_SIZE];
PMSStatus  pmsStatus = PMS_STATUS_WAITING;
PMSData    pmsData;

int mq135RawADC    = 0;
int mq136RawADC    = 0;
int micsRedRawADC  = 0;
int micsNoxRawADC  = 0;
int mp135RawADC    = 0;

int         currentAQI = 0;
const char* currentAQICategory = "N/A";

// ===========================================================================
// FUNCTION PROTOTYPES
// ===========================================================================

void        readPMS5003();
void        readGasSensors();
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
  Serial.println(F("AirGuard system initializing..."));
  Serial.println();
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
// FUNCTION: readPMS5003()
// Reads and validates one complete PMS5003 32-byte packet within a bounded
// timeout window. Sets pmsStatus and, on success, populates pmsData.
// ===========================================================================

void readPMS5003() {
  unsigned long startTime   = millis();
  bool          anyByteSeen = false;
  uint8_t       index       = 0;

  // Poll UART2 until either a full packet is captured or the timeout expires.
  while ((millis() - startTime) < PMS_READ_TIMEOUT_MS) {
    if (PMS.available() > 0) {
      uint8_t incomingByte = (uint8_t)PMS.read();
      anyByteSeen = true;

      if (index == 0) {
        // Looking for first header byte
        if (incomingByte == PMS_START_BYTE_1) {
          pmsBuffer[index++] = incomingByte;
        }
        // Any other byte is discarded while unsynchronized
      } else if (index == 1) {
        // Looking for second header byte
        if (incomingByte == PMS_START_BYTE_2) {
          pmsBuffer[index++] = incomingByte;
        } else {
          index = 0; // Resynchronize
        }
      } else {
        // Collecting remaining packet bytes (buffer overflow prevented by bound)
        if (index < PMS_PACKET_SIZE) {
          pmsBuffer[index++] = incomingByte;
        }
        if (index >= PMS_PACKET_SIZE) {
          break; // Full packet captured
        }
      }
    }
  }

  // ---- No data received at all: sensor is not wired / not powered ----
  if (!anyByteSeen) {
    pmsStatus = PMS_STATUS_NOT_DETECTED;
    return;
  }

  // ---- Timed out mid-packet: sensor present but data incomplete ----
  if (index < PMS_PACKET_SIZE) {
    pmsStatus = PMS_STATUS_WAITING;
    return;
  }

  // ---- Header Validation (defensive re-check) ----
  if (pmsBuffer[0] != PMS_START_BYTE_1 || pmsBuffer[1] != PMS_START_BYTE_2) {
    pmsStatus = PMS_STATUS_INVALID_HEADER;
    return;
  }

  // ---- Checksum Validation ----
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

  // ---- Decode Payload (Atmospheric Environment values, bytes 10-27) ----
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
// FUNCTION: readGasSensors()
// Reads raw 12-bit ADC values from all analog gas sensor channels.
// No ppm conversion is performed since calibration data is unavailable.
// ===========================================================================

void readGasSensors() {
  mq135RawADC   = analogRead(MQ135_PIN);
  mq136RawADC   = analogRead(MQ136_PIN);
  micsRedRawADC = analogRead(MICS_RED_PIN);
  micsNoxRawADC = analogRead(MICS_NOX_PIN);
  mp135RawADC   = analogRead(MP135_PIN);
}

// ===========================================================================
// FUNCTION: calculateAQI()
// Computes the official US EPA Air Quality Index from a PM2.5 concentration
// (µg/m3) using linear interpolation across the standard breakpoint table.
// ===========================================================================

int calculateAQI(float pm25) {
  // EPA convention: truncate PM2.5 to one decimal place before lookup
  float concentration = floorf(pm25 * 10.0f) / 10.0f;

  if (concentration < 0.0f) {
    concentration = 0.0f;
  }
  if (concentration > PM25_BREAKPOINTS[6].concHigh) {
    concentration = PM25_BREAKPOINTS[6].concHigh; // Clamp to Hazardous ceiling
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

  return 500; // Fallback: should be unreachable due to clamping above
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

  // ---- PMS5003 Section ----
  Serial.println(F("PMS5003"));
  Serial.println();

  switch (pmsStatus) {
    case PMS_STATUS_NOT_DETECTED:
      Serial.println(F("PMS5003 Not Detected"));
      break;
    case PMS_STATUS_INVALID_HEADER:
      Serial.println(F("PMS5003 Invalid Packet"));
      break;
    case PMS_STATUS_CHECKSUM_ERROR:
      Serial.println(F("PMS5003 Checksum Error"));
      break;
    case PMS_STATUS_WAITING:
      Serial.println(F("Waiting for PMS5003..."));
      break;
    case PMS_STATUS_OK:
      // Values printed below
      break;
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

  // ---- Gas Sensors Section ----
  Serial.println(F("Gas Sensors"));
  Serial.println();
  Serial.printf("%-20s : %d\n", "MQ135 Raw ADC",    mq135RawADC);
  Serial.printf("%-20s : %d\n", "MQ136 Raw ADC",    mq136RawADC);
  Serial.printf("%-20s : %d\n", "MiCS RED Raw ADC", micsRedRawADC);
  Serial.printf("%-20s : %d\n", "MiCS NOX Raw ADC", micsNoxRawADC);
  Serial.printf("%-20s : %d\n", "MP135 Raw ADC",    mp135RawADC);
  Serial.println();

  // ---- Estimated Values Section (Explicitly Not Calibrated) ----
  Serial.println(F("Estimated Values"));
  Serial.println();
  Serial.printf("%-20s : Not calibrated\n", "CO2");
  Serial.printf("%-20s : Not calibrated\n", "CO");
  Serial.printf("%-20s : Not calibrated\n", "NO2");
  Serial.printf("%-20s : Not calibrated\n", "VOC");
  Serial.printf("%-20s : Not calibrated\n", "NH3");
  Serial.printf("%-20s : Not calibrated\n", "H2S");
  Serial.println();

  // ---- Air Quality Section ----
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
