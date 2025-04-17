import RPi.GPIO as GPIO
import time

# TEST PARAMETERS
PWM = 100  # Duty cycle percentage

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
        pwm.ChangeDutyCycle(PWM)

except KeyboardInterrupt:
    # Stop PWM on interrupt (Ctrl+C)
    pwm.stop()
    GPIO.cleanup()  # Clean up GPIO settings
