import RPi.GPIO as GPIO
import time

from controller_class import Controller

class Motor:
    def __init__(self, pins, set_speed=0, controller=None, encoder=None, pwm_frequency=1000):
        # Self Variable Declarations and Assignments
        self.set_speed = set_speed
        self.speed = 0
        self.PWM = 0
        self.pwm_frequency = pwm_frequency
        self.controller = Controller(coefficients=[1, 0, 0])
        self.encoder = encoder
        self.pins = {}
        #self.pins = {pin_name: pin_number for pin_name, pin_number in pins} is this what you want?

        # Pin Setup
        for pin_name, pin_number in pins:
            GPIO.setup(pin_number, GPIO.OUT)
            self.pins[pin_name] = GPIO.PWM(pin_number, pwm_frequency)
        
        # Start PWM Pins
        for pin_name in self.pins:
            self.pins[pin_name].start(0)

    def calc_PWM(self, set_speed, encoder=None, controller=None):
        # Calculate PWM from PID controller. Encoder feedback is used to adjust the PWM signal.
        self.speed = encoder.get_speed() #need to add encoder paramaters here
        error = set_speed - self.speed
        self.PWM = Controller.calculate_pwm(error) #need to add controller paramaters here

        return self.PWM
    
    def set_motor_speed(self):
        # Set the motor speed using PWM. The speed is set based on the calculated PWM value.
        for pin_name in self.pins:
            self.pins[pin_name].ChangeDutyCycle(self.PWM)
        return
    
    def stop_motor(self):
        # Stop the motor by setting the PWM signal to 0.
        for pin_name in self.pins:
            self.pins[pin_name].ChangeDutyCycle(0)
        return
    
    def get_speed(self):
        # Get the current speed of the motor. This is usually obtained from the encoder.
        self.speed = self.encoder.get_speed() #need to add encoder paramaters here
        return self.speed
    
    def cleanup(self):
        # Cleanup the GPIO pins when done. This is important to avoid warnings and errors when re-running the code.
        for pin_name in self.pins:
            self.pins[pin_name].stop()
        GPIO.cleanup()
        return