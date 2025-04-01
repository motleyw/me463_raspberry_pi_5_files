import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(19, GPIO.OUT)  # Set GPIO pin 17 as an output

# Create a PWM instance on pin 17
pwm = GPIO.PWM(19, 1000)  # 1000 Hz frequency

# Start PWM with a 0% duty cycle (off)
pwm.start(0)

try:
    while True:
        # Increase duty cycle from 0 to 100%
        for i in range(0, 100):
            pwm.ChangeDutyCycle(i)
            time.sleep(.1)
            print(i)
        for i in range(100, 0, -1):
            pwm.ChangeDutyCycle(i)
            print(i)
            time.sleep(.1)

except KeyboardInterrupt:
    # Stop PWM on interrupt (Ctrl+C)
    pwm.stop()
    GPIO.cleanup()  # Clean up GPIO settings
