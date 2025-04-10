import smbus
import time
import RPi.GPIO as GPIO

# # Enable internal pull-ups on GPIO 2 and 3
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # SDA
# GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # SCL

# I2C address and registers for MPU6050
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B

# Initialize I2C bus (bus 1 for Pi 5)
bus = smbus.SMBus(1)

# Wake up MPU6050 by writing 0 to power management register (0x6B)
bus.write_byte_data(0x68, 0x6B, 0)  # 0x68 is the address for MPU6050

# Wake up MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    return value if value < 0x8000 else -((65535 - value) + 1)

while True:
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)

    print(f"Accel X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
    time.sleep(0.5)
