import RPi.GPIO as GPIO
import time
from component_modules.encoder_class import Encoder
from component_modules.motor_class import Motor
from component_modules.controller_class import Controller

#PARAMETERS
drum_PWM = 70
flywheel_PWM = 90
PWM = 30

data = []
start_time = time.time()

left_encoder = Encoder(pin_a=21, pin_b=22)
right_encoder = Encoder(pin_a=23, pin_b=24)
left_encoder.start()
right_encoder.start()

left_motor = Motor(pins={"forward": 13, "backward": 12}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=left_encoder, pwm_frequency=1000, min=20)
right_motor = Motor(pins={"forward": 18, "backward": 20}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=right_encoder, pwm_frequency=1000, min=20)

left_motor.PWM = 1.2 * PWM
right_motor.PWM = PWM


drum_motor = Motor({"forward":19}, set_speed=0, coefficients=[-6.9932, 4.4445, -343.31, 32.46], c_type="FF_2", encoder=None, pwm_frequency=1000, min=20)
flywheel_motor = Motor({"forward":17}, set_speed=0, coefficients=[3.8739, 0.1569], c_type="FF_1", encoder=None, pwm_frequency=1000, min=32)

drum_motor.PWM = drum_PWM
flywheel_motor.PWM = flywheel_PWM

flywheel_motor.set_motor_speed()

time.sleep(3)

left_motor.set_motor_speed()
right_motor.set_motor_speed()

drum_motor.set_motor_speed()

time.sleep(20)

right_encoder.stop()
left_encoder.stop()
left_motor.stop_motor()
right_motor.stop_motor()
left_motor.cleanup()
right_motor.cleanup()
drum_motor.stop_motor()
drum_motor.cleanup()
flywheel_motor.stop_motor()
flywheel_motor.cleanup()
GPIO.cleanup()
