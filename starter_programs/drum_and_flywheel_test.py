import RPi.GPIO as GPIO
import time

# Set up GPIO mode
# Flywheel
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(17, GPIO.OUT)  # Set GPIO pin 17 as an output
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(19, GPIO.OUT)  # Set GPIO pin 19 as an output

# Create a PWM instance on pin 17
pwm1 = GPIO.PWM(17, 1000)  # 1000 Hz frequency
pwm2 = GPIO.PWM(19, 1000)  # 1000 Hz frequency

# Start PWM with a 0% duty cycle (off)
pwm1.start(0)
pwm2.start(0)

try:
    while True:
        # Increase duty cycle from 0 to 100%
        for i in range(0, 100):
            pwm1.ChangeDutyCycle(i)
            pwm2.ChangeDutyCycle(i)
            time.sleep(.1)
            print(i)
        for i in range(100, 0, -1):
            pwm1.ChangeDutyCycle(i)
            pwm2.ChangeDutyCycle(i)
            print(i)
            time.sleep(.1)

except KeyboardInterrupt:
    # Stop PWM on interrupt (Ctrl+C)
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()  # Clean up GPIO settings
