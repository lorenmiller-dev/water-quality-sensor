import serial
import pandas as pd
import time
import re  # Regular expression library for data parsing

# Serial port configuration
serial_port = "/dev/tty.usbmodem101"
baud_rate = 115200
timeout = 2

# Attempt to establish serial connection
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    print("Serial connection established.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Data rows
data = []

try:
    # Wait for Arduino to reset and start sending data
    time.sleep(2)  # Increase this if data is delayed

    while True:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').strip()

        # Debugging output to check if a line is received
        if line:
            print("Raw Data Line:", line)  # Print the received line from Arduino

            # Regular expression to match the format: "Temperature: 20.94 °C | TDS Value: 0.00 ppm | pH: 6.67"
            match = re.search(
                r"Temperature:\s*([-+]?\d*\.\d+|\d+)\s*°C\s*\|\s*TDS Value:\s*([-+]?\d*\.\d+|\d+)\s*ppm\s*\|\s*pH:\s*([-+]?\d*\.\d+|\d+)",
                line)

            if match:
                try:
                    # Extract temperature, TDS, and pH values from the matched groups
                    temp = float(match.group(1))
                    tds_value = float(match.group(2))
                    ph_value = float(match.group(3))

                    # Append to data list as a dictionary
                    data.append({
                        'Temperature (°C)': temp,
                        'TDS Value (ppm)': tds_value,
                        'pH': ph_value
                    })
                except ValueError:
                    print("Error converting data:", line)
            else:
                print("Data format mismatch:", line)

        else:
            print("Empty line received")  # Indicates no data or timeout

        # Stop after 10 readings for this example
        if len(data) > 1000:
            break

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    # Ensure the serial connection is closed properly
    ser.close()
    print("Serial connection closed.")

# Convert collected data into a pandas DataFrame
print("Collected Data:", data)  # Debug print to check the data list
df = pd.DataFrame(data)

# Save to CSV or analyze the DataFrame
df.to_csv('arduino_data.csv', index=False)
print("Data saved to arduino_data.csv")
print(df)