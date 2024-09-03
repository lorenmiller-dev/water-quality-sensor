import serial
import pandas as pd
import time

serial_port = "/dev/tty.usbmodem2101"
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
            print(line)  # Print raw data

            values = line.split(',')

            if len(values) == 4:
                temp, DO, adc_raw, adc_voltage = values
                data.append({
                    'Temperature': float(temp),
                    'Dissolved Oxygen': float(DO),
                    'ADC Raw': int(adc_raw),
                    'ADC Voltage (mV)': float(adc_voltage)
                })

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()  # Ensure the serial connection is closed properly

# Convert collected data into a pandas DataFrame
df = pd.DataFrame(data)

# Save to CSV or analyze the DataFrame
df.to_csv('arduino_data.csv', index=False)
print("Data saved to arduino_data.csv")
print(df)
