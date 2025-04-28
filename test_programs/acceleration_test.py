import RPi.GPIO as GPIO
import time
import csv
from component_modules.encoder_class import Encoder
from component_modules.motor_class import Motor
from component_modules.controller_class import Controller

try:
    #PARAMETERS
    # MOTOR LEFT pins: 12 backward, 13 forward
    # MOTOR RIGHT pins: 20 backward, 18 forward
    PWM = 70
    duration = 30  # (s)
    direction = "forward"
    filename = "output_data/stopping_test/PWM90_test2.csv"

    data = []
    start_time = time.time()

    left_encoder = Encoder(pin_a=21, pin_b=22)
    right_encoder = Encoder(pin_a=23, pin_b=24)
    left_encoder.start()
    right_encoder.start()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)
    GPIO.output(6, GPIO.HIGH)

    left_motor = Motor(pins={"forward": 13, "backward": 12}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=left_encoder, pwm_frequency=1000, min=20)
    right_motor = Motor(pins={"forward": 18, "backward": 20}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=right_encoder, pwm_frequency=1000, min=20)

    left_motor.PWM = 1.2 * PWM
    right_motor.PWM = PWM

    left_motor.set_motor_speed()
    right_motor.set_motor_speed()

    for i in range(100 * duration):
        elapsed_time = time.time() - start_time
        right_speed = right_encoder.speed()
        left_speed = left_encoder.speed()
        data.append([elapsed_time, left_speed, right_speed])
        print(f"Left: {left_speed}, Right: {right_speed}")
        time.sleep(0.1)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Left Wheel Speed (rad/s)', 'Right Wheel Speed (rad/s)'])  # header
        writer.writerows(data)

except KeyboardInterrupt:
    right_encoder.stop()
    left_encoder.stop()
    left_motor.stop_motor()
    right_motor.stop_motor()
    left_motor.cleanup()
    right_motor.cleanup()
    GPIO.cleanup()
