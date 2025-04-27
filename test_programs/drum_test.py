import RPi.GPIO as GPIO
import time
from component_modules.encoder_class import Encoder
from component_modules.motor_class import Motor
from component_modules.controller_class import Controller

#PARAMETERS
PWM = 99

data = []
start_time = time.time()

drum_motor = Motor({"forward":19}, set_speed=0, coefficients=[-6.9932, 4.4445, -343.31, 32.46], c_type="FF_2", encoder=None, pwm_frequency=1000, min=20)

drum_motor.PWM = PWM

drum_motor.set_motor_speed()

time.sleep(10)

drum_motor.stop_motor()
drum_motor.cleanup()
GPIO.cleanup()
