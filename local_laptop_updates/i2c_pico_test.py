import serial

ser = serial.Serial("/dev/ttyAMA3", 115200, timeout=1)

while True:
    data = ser.read(1)
    print(data)
    if data:
        byte_val = int.from_bytes(data, "big")
        speed_val = (byte_val >> 2) & 0x3F
        fill_level = byte_val & 0x03
        print(f"Speed adj: {speed_val}/63, Fill level: {fill_level}")
