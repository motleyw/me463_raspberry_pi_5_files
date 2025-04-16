##########################################################################################
# Main file for the Raspberry Pi Pico project
# This file contains the main loop that runs the ultrasoncic sensors and communicates with the Raspberry Pi 5
# Main structure is that the main loop reads all the ultrasonic sensors, computes the speed adjustment and sends it to the RPi 5.
##########################################################################################

import time
import threading
import RPi.GPIO as GPIO
import motor_class as mc
import ultrasonic_class as uc

# Instantiate the classes - 7 ultrasonic sensors and the Pico
# ULTS1 is left most, ULTS7 is right most
ULTS1 = uc.ULTSensor(trigger_pin=23, echo_pin=24) #Update pin numbers
ULTS2 = uc.ULTSensor(trigger_pin=25, echo_pin=26) #Update pin numbers
ULTS3 = uc.ULTSensor(trigger_pin=27, echo_pin=28) #Update pin numbers
ULTS4 = uc.ULTSensor(trigger_pin=29, echo_pin=30) #Update pin numbers
ULTS5 = uc.ULTSensor(trigger_pin=31, echo_pin=32) #Update pin numbers
ULTS6 = uc.ULTSensor(trigger_pin=33, echo_pin=34) #Update pin numbers
ULTS7 = uc.ULTSensor(trigger_pin=35, echo_pin=36) #Update pin numbers

speed_adjustment = 1
stop = False

while True:
    if (stop):
        break
    else:
        # Read the ultrasonic sensors
        dist1 = ULTS1.measure_distance()
        dist2 = ULTS2.measure_distance()
        dist3 = ULTS3.measure_distance()
        dist4 = ULTS4.measure_distance()
        dist5 = ULTS5.measure_distance()
        dist6 = ULTS6.measure_distance()
        dist7 = ULTS7.measure_distance()

        # Outer sensors (1&7) adjust speed adjustment proportionally between 36 and 20cm
        # Middle sensors (2&6) adjust speed adjustment proportionally between 33 and 20cm
        # Inner sensors (3&4&5) adjust speed adjustment proportionally between 30 and 20cm
        if (dist1 < 36):
            speed_adjustment = (dist1 - 20) / (36 - 20)
        if (dist2 < 33):
            speed_adjustment = (dist2 - 20) / (33 - 20)
        if (dist3 < 30):
            speed_adjustment = (dist3 - 20) / (30 - 20)
        if (dist4 < 30):
            speed_adjustment = (dist4 - 20) / (30 - 20)
        if (dist5 < 30):
            speed_adjustment = (dist5 - 20) / (30 - 20)
        if (dist6 < 33):
            speed_adjustment = (dist6 - 20) / (33 - 20)
        if (dist7 < 36):
            speed_adjustment = (dist7 - 20) / (36 - 20)
        if (dist1 < 20 or dist2 < 20 or dist3 < 20 or dist4 < 20 or dist5 < 20 or dist6 < 20 or dist7 < 20):
            speed_adjustment = 0

        # If any sensor is greater than its threshold, set speed adjustment to 1s
        # If any sensor is less than 20cm, set speed adjustment to 0s
        if (speed_adjustment < 0):
            speed_adjustment = 0
        if (speed_adjustment > 1):
            speed_adjustment = 1

        # Send the speed adjustment to the RPi 5 through I2C

