import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SPEED_ADJUSTMENT = 9
FILL_LEVEL = 8

# Set input without pull-up/down since Pico is actively driving it
GPIO.setup(SPEED_ADJUSTMENT, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(FILL_LEVEL, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

try:
    while True:
        print(GPIO.input(SPEED_ADJUSTMENT) == GPIO.HIGH)
        print(GPIO.input(FILL_LEVEL) == GPIO.HIGH)
        time.sleep(0.1)
finally:
    GPIO.cleanup()
