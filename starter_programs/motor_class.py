import RPi.GPIO as GPIO
import time

from controller_class import Controller
from encoder_class import Encoder

class Motor:
    def __init__(self, pins, set_speed=0, coefficients=[], c_type="PID", encoder=None, pwm_frequency=1000, min=0):
        # Self Variable Declarations and Assignments
        self.set_speed = set_speed
        self.speed = 0
        self.PWM = 0
        self.pwm_frequency = pwm_frequency
        self.type = c_type
        self.controller = Controller(coefficients, c_type, min)
        self.encoder = encoder
        self.pins = {}  # Make sure 2nd pin is the backwards pin

        if ("type"=="PID"):
            self.encoder.start()

        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

        # Pin Setup
        for pin_name in pins:
            #print(pins[pin_name])
            GPIO.setup(pins[pin_name], GPIO.OUT)
            self.pins[pin_name] = GPIO.PWM(pins[pin_name], pwm_frequency)
        
        # Start PWM Pins
        for pin_name in self.pins:
            self.pins[pin_name].start(0)
    
    def calc_PWM(self, set_speed):
        # Calculate PWM from controller. Encoder feedback is used to adjust the PWM signal.
        if (self.type=="PID"):
            self.encoder.update()
            self.speed = self.encoder.speed() #rad/s
            error = set_speed - self.speed
        elif (self.type=="FF_1" or self.type=="FF_2"):
            error = set_speed
        self.PWM = self.controller.calculate_pwm(error, 0.001) #dt = 1ms
        return self.PWM
    
    def set_motor_speed(self):
        # Set the motor speed using PWM. The speed is set based on the calculated PWM value.
        print(self.PWM)
        if self.PWM < 0:
            print("Backward")
            self.pins["backward"].ChangeDutyCycle(-self.PWM)
        else:
            print("Forward")
            self.pins["forward"].ChangeDutyCycle(self.PWM)

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