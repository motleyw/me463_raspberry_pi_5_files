import RPi.GPIO as GPIO
import time
import csv
from component_modules.encoder_class import Encoder
from component_modules.motor_class import Motor
from component_modules.controller_class import Controller
from component_modules.imu_class import IMU

#PARAMETERS
# MOTOR LEFT pins: 12 backward, 13 forward
# MOTOR RIGHT pins: 20 backward, 18 forward
PWM = 99
duration = 10  # (s)
direction = "forward"
filename = "output_data/imu_tests/30PWM_test1.csv"

data = []
start_time = time.time()

left_encoder = Encoder(pin_a=21, pin_b=22)
right_encoder = Encoder(pin_a=23, pin_b=24)
imu = IMU()
left_encoder.start()
right_encoder.start()
imu.start()

left_motor = Motor(pins={"forward": 13, "backward": 12}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=left_encoder, pwm_frequency=1000, min=20)
right_motor = Motor(pins={"forward": 18, "backward": 20}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=right_encoder, pwm_frequency=1000, min=20)

left_motor.PWM = PWM
right_motor.PWM = PWM

left_motor.set_motor_speed()
right_motor.set_motor_speed()

for i in range(100 * duration):
    elapsed_time = time.time() - start_time
    right_speed = right_encoder.speed()
    left_speed = left_encoder.speed()

    current_acceleration = list(imu.get_acceleration().values())

    data.append([elapsed_time, left_speed, right_speed] + current_acceleration)

    time.sleep(0.01)

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Left Wheel Speed (rad/s)', 'Right Wheel Speed (rad/s)', 'X Acceleration', 'Y Acceleration', 'Z Acceleration', 'X Gyro', 'Y Gyro', 'Z Gyro'])  # header
    writer.writerows(data)

right_encoder.stop()
left_encoder.stop()
left_motor.stop_motor()
right_motor.stop_motor()
left_motor.cleanup()
right_motor.cleanup()
GPIO.cleanup()
