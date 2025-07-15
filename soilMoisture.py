import serial
import time
import re
from datetime import datetime

# Serial port and settings
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Allow Arduino to reset

# Moisture calibration values (adjust based on your sensor)
DRY_VALUE = 1023  # Value in air
WET_VALUE = 200   # Value fully submerged

# Open file for logging
with open("moisture_log.txt", "a") as logfile:
    print("Reading soil moisture sensor... Logging to moisture_log.txt")
    
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            
            # Only process non-empty lines
            if line:
                # print(f"RAW LINE: {line}")  # Debug output - commented out
                
                # Updated regex pattern to match "Analog Value: 1023"
                match = re.search(r'Analog Value:\s*(\d+)', line)
                
                if match:
                    raw_value = int(match.group(1))
                    moisture = (DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE) * 100
                    moisture = max(0, min(100, moisture))  # Clamp to 0–100%
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    output = f"{timestamp} - Raw: {raw_value} -> Soil moisture: {moisture:.1f}%"
                    print(output)
                    logfile.write(output + "\n")
                    logfile.flush()
                # Remove the "Ignored" message to reduce clutter
                # else:
                #     print("Ignored: No match in line")
                
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")