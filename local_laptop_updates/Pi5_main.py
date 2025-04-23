##########################################################################################
# Main file for the Raspberry Pi 5 project
# This file contains the main loop that runs the sensors, motors, and handles the GPIO pins
# Main structure is that the HMI decides which case to run and the main loop runs the case
# The main loop runs the sensors, motors, and handles the GPIO pins
##########################################################################################


import RPi.GPIO as GPIO
import time
import threading
from motor_class import Motor
from imu_class import IMU
from lcd_class import LCD
# from gps_class import GPS
# from lcd_class import LCD

# Left Drive Motor Parameters
motorL_Kp = 0.1
motorL_Ki = 0.01
motorL_Kd = 0.01
motorL_coef = [motorL_Kp, motorL_Ki, motorL_Kd]

# Right Drive Motor Parameters
motorR_Kp = 0.1
motorR_Ki = 0.01
motorR_Kd = 0.01
motorR_coef = [motorR_Kp, motorR_Ki, motorR_Kd]

# Instatntiate the classes
# create Rpi, HMI, motors, IMU, GPS, Pico, and other classes here
lcd = LCD(i2c_address=0x27, bus_number=1)  # Example I2C address and bus number


# Define GPIO pins for your buttons
UP_BUTTON = 7        # GPIO pin for the "up" button
DOWN_BUTTON = 5      # GPIO pin for the "down" button
SELECT_BUTTON = 1    # GPIO pin for the "select" button

# Mode setup
modes = ['Idle', 'BTC', 'Mapping', 'Auto', 'Demo']
current_mode_index = 0
idle_toggle = True    # Keeps track of whether we're in the idle state or an active mode

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SELECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup_gpio():
    GPIO.cleanup()

def read_button():
    # Check if the UP button is pressed
    if GPIO.input(UP_BUTTON) == GPIO.LOW:
        return 'u'
    # Check if the DOWN button is pressed
    elif GPIO.input(DOWN_BUTTON) == GPIO.LOW:
        return 'd'
    # Check if the SELECT button is pressed
    elif GPIO.input(SELECT_BUTTON) == GPIO.LOW:
        return 's'
    return None

def handle_menu_case(index):
    match modes[index]:
        case "Idle":
            if idle_toggle:
                lcd.write("Idle Mode", 1, 1)
            else:
                print("Running Idle mode...")
                lcd.write("Idle Mode", 1, 1)
                lcd.write("Running...", 2, 1)
                #do Idle mode tasks here
        case "BTC":
            if idle_toggle:
                lcd.write("BTC Mode", 1, 1)
            else:
                print("Running BTC mode...")
                lcd.write("BTC Mode", 1, 1)
                lcd.write("Running...", 2, 1)
                #do BTC mode tasks here
        case "Mapping":
            if idle_toggle:
                lcd.write("Mapping Mode", 1, 1)
            else:
                print("Running Mapping mode...")
                lcd.write("Mapping Mode", 1, 1)
                lcd.write("Running...", 2, 1)
                #do Mapping mode tasks here
        case "Auto":
            if idle_toggle:
                lcd.write("Auto Mode", 1, 1)
            else:
                print("Running Auto mode...")
                lcd.write("Auto Mode", 1, 1)
                lcd.write("Running...", 2, 1)
                #do Auto mode tasks here
        case "Demo":
            if idle_toggle:
                lcd.write("Demo Mode", 1, 1)
            else:
                print("Running Demo mode...")
                lcd.write("Demo Mode", 1, 1)
                lcd.write("Running...", 2, 1)  
                #do Demo mode tasks here
        case _:
            print("Invalid menu selection.")

def main():
    global current_menu_index
    print("Starting menu navigation...\n")

    while True:
        print(f"\nCurrent Menu: {modes[current_menu_index]}")
        handle_menu_case(current_menu_index)

        button = read_button()

        if button == "u":
            current_menu_index = (current_menu_index + 1) % len(modes)
        elif button == "d":
            current_menu_index = (current_menu_index - 1) % len(modes)
        elif button == "s":
            print(f"Selected: {modes[current_menu_index]}")
            idle_toggle = not idle_toggle  # Toggle the idle state
            
        # Optional: add small delay for readability/debouncing
        time.sleep(0.1)

if __name__ == "__main__":
    main()