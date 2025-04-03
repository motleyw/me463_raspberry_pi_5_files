import serial
import time
import re

# Open serial port for GPS communication (UART3 is usually /dev/serial0)
gps_port = "/dev/ttyAMA0"  # Change to "/dev/ttyS0" if needed
baud_rate = 9600  # Standard baud rate for NEO-6M

try:
    ser = serial.Serial(gps_port, baud_rate, timeout=1)
    print("Listening for GPS data...")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

def parse_gps(sentence):
    """Extracts latitude and longitude from an NMEA sentence."""
    if sentence.startswith("$GPGGA"):  # Check if it's a GPGGA sentence
        fields = sentence.split(",")
        if len(fields) > 6 and fields[2] and fields[4]:  # Ensure valid data
            lat = convert_to_degrees(fields[2])
            lat_dir = fields[3]
            lon = convert_to_degrees(fields[4])
            lon_dir = fields[5]
            return f"Latitude: {lat} {lat_dir}, Longitude: {lon} {lon_dir}"
    return "No valid GPS data."

def convert_to_degrees(raw_value):
    """Convert NMEA coordinate format (DDMM.MMMM) to decimal degrees."""
    try:
        d = int(float(raw_value) / 100)  # Extract degrees
        m = float(raw_value) % 100 / 60  # Convert minutes to degrees
        return round(d + m, 6)
    except ValueError:
        return None

# Continuously read GPS data
try:
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:  # Look for valid GPS sentences
            print(parse_gps(line))
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping GPS reading...")
    ser.close()
