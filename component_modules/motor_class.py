import RPi.GPIO as GPIO
import time

class Motor:
    def __init__(self, pins, set_speed=0, controller=None, encoder=None, pwm_frequency=1000):
        # Self Variable Declarations and Assignments
        self.set_speed = set_speed
        self.speed = speed
        self.controller = controller
        self.encoder = encoder
        self.pins = {}

        # Pin Setup
        for pin_name, pin_number in pins:
            GPIO.setup(pin_number, GPIO.OUT)
            self.pins[pin_name] = GPIO.PWM(pin_number, pwm_frequency)
        
        # Start PWM Pins
        for pin_name in self.pins:
            self.pins[pin_name].start(0)
        
    def set_motor_speed(self, set_speed):
        PWM_limit = 25
        