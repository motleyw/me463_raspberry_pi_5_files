import RPi.GPIO as GPIO
import smbus2
import time

I2C_SLAVE_ADDR = 0x42  # Same address as in the Pico slave code

bus = smbus2.SMBus(3)  # Initialize the I2C bus (1 means the Pi's I2C bus)

while True:
    # Read the response from Pico (up to 64 bytes)
    response = bus.read_i2c_block_data(I2C_SLAVE_ADDR, 0, 32)
    print("Received:", response)
    time.sleep(1)



"""
# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(17, GPIO.OUT)  # Set GPIO pin 17 as an output


# Create a PWM instance on pin 17
pwm = GPIO.PWM(17, 1000)  # 1000 Hz frequency

# Start PWM with a 0% duty cycle (off)
pwm.start(0)

try:
    while True:
        # Increase duty cycle from 0 to 100%
        pwm.ChangeDutyCycle(100)

except KeyboardInterrupt:
    # Stop PWM on interrupt (Ctrl+C)
    pwm.stop()
    GPIO.cleanup()  # Clean up GPIO settings
"""