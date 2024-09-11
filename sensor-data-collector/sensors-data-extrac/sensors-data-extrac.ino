// Temperature and Total Dissolved Solids (TDS) sensors data extractors
// Library imports
#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
#include <GravityTDS.h>

// Sensor pin assignments
#define TdsSensorPin A1        // TDS sensor connected to analog pin A1
#define TempSensorPin A2        // Digital pin for DS18B20 temperature sensor
#define PhSensorPin A0         // pH sensor connected to analog pin A0

// DS18B20 temperature setup
OneWire oneWire(TempSensorPin);
DallasTemperature sensors(&oneWire);

// Gravity TDS sensor setup
GravityTDS gravityTds;  // Create a TDS object

// Configurable parameters
float analogReferenceVoltage = 5.0; // Analog reference voltage (V)
int adcResolution = 1024;           // ADC resolution
float defaultTemperature = 25.0;    // Default initial temperature
float phSlope = 3.5;                // pH sensor calibration slope
float phOffset = -1.6;              // pH sensor calibration offset

// Initial temperature value (will be updated)
float temperature = defaultTemperature;

void setup() {
  // 115200 baud rate
  Serial.begin(115200);

  // Initialize DS18B20 temperature sensor
  sensors.begin();
  
  // Initialize Gravity TDS sensor
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(analogReferenceVoltage);  // Set analog reference voltage
  gravityTds.setAdcRange(adcResolution);       // Set ADC resolution
  gravityTds.begin();
}

void loop() {
  // --- Temperature Sensor Reading ---
  sensors.requestTemperatures();
  temperature = sensors.getTempCByIndex(0); // Read temperature in Celsius

  // Check if the temperature is valid
  if (temperature == DEVICE_DISCONNECTED_C) {
    Serial.println("Error: Could not read temperature data");
    return;  // Exit loop iteration if no valid temperature
  } 

  // --- TDS Sensor Reading ---
  gravityTds.setTemperature(temperature);  // Update TDS sensor with the current temperature for compensation
  gravityTds.update();  // Update the TDS reading
  float tdsValue = gravityTds.getTdsValue();  // Get the TDS value in ppm

  // --- pH Sensor Reading ---
  int buf[10];  // Buffer to store 10 samples for averaging
  unsigned long int avgValue = 0;
  for (int i = 0; i < 10; i++) { // Collect 10 samples from the pH sensor
    buf[i] = analogRead(PhSensorPin);
    delay(10);
  }

  for (int i = 0; i < 10; i++) { 
    avgValue += buf[i];
  }

  avgValue /= 10;  // Calculate average
  float voltage = avgValue * analogReferenceVoltage / adcResolution;  // Convert the average reading to voltage

  // Convert voltage to pH using calibration values
  float pH = (phSlope * voltage) + phOffset;

  // --- Output Readings to Serial Monitor ---
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C | TDS Value: ");
  Serial.print(tdsValue);
  Serial.print(" ppm | pH: ");
  Serial.println(pH);

  // Wait before taking another reading
  delay(1000);
}


