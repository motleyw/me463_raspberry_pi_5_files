import RPi.GPIO as GPIO
import time

class Motor:
    def __init__(self, pins, speed=0):
        self.speed = speed
        self.pins = pins
