# Class for Ultrasonic Sensor
# This class is designed to be used with the Raspberry Pi GPIO library
# and is intended to be used with a multipe ultrasonic sensors.
# The class handles the setup and measurement of distance using the ultrasonic sensor.

import RPi.GPIO as GPIO
import time

class ULTSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.distance = 0
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        # Calculate distance in cm
        elapsed_time = stop_time - start_time
        self.distance = (elapsed_time * 34300) / 2
        return self.distance

    def get_distance(self):
        return self.distance    