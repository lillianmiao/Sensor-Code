import serial
import time

# Change this to your Arduino's serial port
SERIAL_PORT = '/dev/ttyACM1'  # or 'COM3' on Windows
BAUD_RATE = 9600              # Must match Serial.begin(9600) on Arduino

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        time.sleep(2)  # Wait for Arduino to reset on connection

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line and line.startswith("distance"):
                print(f"Received: {line}")
                parts = line.split()
                try:
                    dist = int(parts[2])
                    strength = int(parts[5])
                    print(f"Distance: {dist}, Strength: {strength}")
                except (IndexError, ValueError):
                    print("Failed to parse data")

    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == '__main__':
    main()
