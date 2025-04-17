import sys
sys.path.append("../local_laptop_updates")
from motor_class import Motor
from controller_class import Controller
import time
import RPi.GPIO as GPIO

# instantiate motor
motor = Motor({"Pin":19}, set_speed=0, coefficients=[-6.9932, 4.4445, -343.31, 32.46], c_type="FF_2", encoder=None, pwm_frequency=1000, min=20)

# Test the set_motor_speed method
try:
    while True:
        motor.calc_PWM(13)
        print(motor.PWM)
        motor.set_motor_speed()
except KeyboardInterrupt:
        print("keyboard interrupt")
        motor.stop_motor()
        motor.cleanup()
        print("cleanup method works correctly.")


# Test the stop_motor method
# try:
#     motor.stop_motor()
#     print("stop_motor method works correctly.")
# except Exception as e:
#     print("stop_motor method failed:", e)

# # Test the get_speed method
# try:
#     motor.get_speed()
#     print("get_speed method works correctly.")
# except Exception as e:
#     print("get_speed method failed:", e)

# # Test the cleanup method
# try:
#     motor.cleanup()
#     print("cleanup method works correctly.")
# except Exception as e:
#     print("cleanup method failed:", e)
