##########################################################################################
# Main file for the Raspberry Pi 5 project
# This file contains the main loop that runs the sensors, motors, and handles the GPIO pins
# Main structure is that the HMI decides which case to run and the main loop runs the case
# The main loop runs the sensors, motors, and handles the GPIO pins
##########################################################################################


import RPi.GPIO as GPIO
import time
import threading


# Instatntiate the classes
# create Rpi, HMI, motors, IMU, GPS, Pico, and other classes here

# main loop starts here and runs as long as no stop command is given
while True:
    if (stop):  # check for stop command
        break
    else:
        # determine which case to run from HMI
        
        # run the case here
        pass



