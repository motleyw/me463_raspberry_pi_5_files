from smbus2 import SMBus

PICO_I2C_ADDR = 0x42

with SMBus(1) as bus:
    while True:
        try:
            data = bus.read_byte(PICO_I2C_ADDR)
            fill_level = data & 0x03
            speed_correction = (data >> 2) / 63.0
            print(f"Speed Correction: {speed_correction}; Fill Level: {fill_level}")
        except Exception as e:
            print("I2C Read Error:", e)
