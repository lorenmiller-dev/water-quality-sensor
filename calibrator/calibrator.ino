// Calibrator

#include <Arduino.h>

#define VREF    5000  // Reference voltage in mV
#define ADC_RES 1024  // ADC resolution

const int baudRate = 9600;     // Baud rate for serial communication
const int delayTime = 1000;    // Delay time in milliseconds
const int analogPin = A0;      // Analog pin to read from

uint32_t raw;

void setup() {
  Serial.begin(baudRate); // Initialize serial communication at 9600 bits/s
}

void loop() {
  raw = analogRead(analogPin);  // Read from the defined analog pin
  float voltage = raw * (VREF / (float)ADC_RES);  // Convert raw data to voltage in mV

  // Construct the output message
  String outputMessage = "Raw: " + String(raw) + "\tVoltage (mV): " + String(voltage, 2);  // Display 2 decimal places

  // Print the output message
  Serial.println(outputMessage);
  
  delay(delayTime);  // Wait for the specified delay time before next reading
}
