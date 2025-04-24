import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SPEED_ADJUSTMENT = 9
FILL_LEVEL = 8
GPIO.setup(SPEED_ADJUSTMENT, GPIO.IN)
GPIO.setup(FILL_LEVEL, GPIO.IN)

while True:
    print(GPIO.input(SPEED_ADJUSTMENT) == GPIO.HIGH)
    print(GPIO.input(FILL_LEVEL) == GPIO.HIGH)
    time.sleep(1)