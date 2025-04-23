import RPi.GPIO as GPIO
import time

#PARAMETERS
# MOTOR LEFT pins: 12 backward, 13 forward
# MOTOR RIGHT pins: 18, 20

PWM = 40
direction = "backward"

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 as an output
GPIO.setup(13, GPIO.OUT)  # Set GPIO pin 13 as an output

# Create a PWM instance on pin 17
pwm_1 = GPIO.PWM(12, 1000)  # 1000 Hz frequency
pwm_2 = GPIO.PWM(13, 1000)  # 1000 Hz frequency

# Start PWM with a 0% duty cycle (off)
pwm_1.start(0)
pwm_2.start(0)

try:
    while True:
        if direction == "forward":
            pwm_2.ChangeDutyCycle(PWM)  # Set duty cycle to 50%
        else:
            pwm_1.ChangeDutyCycle(PWM)
except KeyboardInterrupt:
    # Stop PWM on interrupt (Ctrl+C)
    pwm_1.stop()
    pwm_2.stop()
    GPIO.cleanup()



# try:
#     while True:
#         # Increase duty cycle from 0 to 100%
#         for i in range(0, 100):
#             pwm.ChangeDutyCycle(i)
#             time.sleep(.1)
#             print(i)
#         for i in range(100, 0, -1):
#             pwm.ChangeDutyCycle(i)
#             print(i)
#             time.sleep(.1)

