import serial
import pandas as pd
import time

serial_port = "/dev/tty.usbmodem101"
baud_rate = 115200
timeout = 2

# Establishing serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# Data rows
data = []

try:
    time.sleep(2)

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Raw Data Line:", line)  # Print raw data line

            # Remove labels from the line and split values by the tab or space separator
            line = line.replace("Temperature:", "").replace("ADC RAW:", "").replace("ADC Voltage (mV):", "").replace("DO:", "")
            values = [v.strip() for v in line.split('\t')]

            if len(values) == 3:
                try:
                    temp, adc_raw, adc_voltage, DO = values
                    data.append({
                        'Temperature': float(temp),
                        'Dissolved Oxygen': float(DO),
                        'ADC Raw': int(adc_raw),
                        'ADC Voltage': float(adc_voltage)
                    })
                except ValueError:
                    print("Error converting data:", values)

        if len(data) > 10:  # Stop after 10 readings for this example
            break

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()  # Ensure the serial connection is closed properly

# Convert collected data into a pandas DataFrame
print("Collected Data:", data)  # Debug print to check the data list
df = pd.DataFrame(data)

# Save to CSV or analyze the DataFrame
df.to_csv('arduino_data.csv', index=False)
print("Data saved to arduino_data.csv")
print(df)