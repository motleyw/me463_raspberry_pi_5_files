import smbus
import time

# Create an SMBus instance
bus = smbus.SMBus(1)  # Use I2C bus 1

# MPU6050 device address
MPU6050_ADDR = 0x68

# Wake up the MPU6050 (exit sleep mode)
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)
time.sleep(0.1)  # Give it a moment to wake up

def read_word(reg):
    """Read two bytes and combine them."""
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

while True:
    # Read accelerometer data (registers 0x3B to 0x40)
    accel_x = read_word(0x3B)
    accel_y = read_word(0x3D)
    accel_z = read_word(0x3F)

    # Read gyroscope data (registers 0x43 to 0x48)
    gyro_x = read_word(0x43)
    gyro_y = read_word(0x45)
    gyro_z = read_word(0x47)

    print("Accel [g]: X={:.2f} Y={:.2f} Z={:.2f}".format(
        accel_x / 16384.0, accel_y / 16384.0, accel_z / 16384.0))
    print("Gyro [°/s]: X={:.2f} Y={:.2f} Z={:.2f}".format(
        gyro_x / 131.0, gyro_y / 131.0, gyro_z / 131.0))
    print("-" * 50)

    time.sleep(0.01)
