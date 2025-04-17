##########################################################################################
# Main file for the Raspberry Pi 5 project
# This file contains the main loop that runs the sensors, motors, and handles the GPIO pins
# Main structure is that the HMI decides which case to run and the main loop runs the case
# The main loop runs the sensors, motors, and handles the GPIO pins
##########################################################################################


import RPi.GPIO as GPIO
import time
import threading


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

# Drum Motor Parameters
motorD_Kp = 0.1
motorD_Ki = 0.01
motorD_Kd = 0.01
motorD_coef = [motorD_Kp, motorD_Ki, motorD_Kd]

# Flywheel Motor Parameters
motorF_Kp = 0.1
motorF_Ki = 0.01
motorF_Kd = 0.01
motorF_coef = [motorF_Kp, motorF_Ki, motorF_Kd]




# Instatntiate the classes
# create Rpi, HMI, motors, IMU, GPS, Pico, and other classes here

# Define GPIO pins for your buttons
UP_BUTTON = 17       # GPIO pin for the "up" button
DOWN_BUTTON = 27     # GPIO pin for the "down" button
SELECT_BUTTON = 22   # GPIO pin for the "select" button

# Mode setup
modes = ['Idle', 'BTC', 'Auto_Nav', 'Mode 4']
current_mode_index = 0
idle_state = True    # Keeps track of whether we're in the idle state or an active mode

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SELECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup_gpio():
    GPIO.cleanup()

def cycle_up():
    global current_mode_index
    current_mode_index = (current_mode_index - 1) % len(modes)
    print(f"Selected: {modes[current_mode_index]}")

def cycle_down():
    global current_mode_index
    current_mode_index = (current_mode_index + 1) % len(modes)
    print(f"Selected: {modes[current_mode_index]}")

def enter_mode():
    global idle_state
    idle_state = False
    print(f"Entering {modes[current_mode_index]}...")
    # Here, call the imported method for the selected mode.
    if modes[current_mode_index] == 'Idle':
        idle()  # Replace with idle function
    elif modes[current_mode_index] == 'BTC':
        BTC()   # Replace with BTC function
    elif modes[current_mode_index] == 'Auto_Nav':
        Auto_Nav()  # Replace with Auto_Nav function

def exit_mode():
    global idle_state
    idle_state = True
    print("Returning to idle state...")

def mode_1_function():
    while not GPIO.input(SELECT_BUTTON):  # Exit mode when the "select" button is pressed
        print("Mode 1 is active...")
        time.sleep(0.5)  # Simulate mode functionality
    exit_mode()

def main():
    setup_gpio()
    global idle_state
    try:
        while True:
            if idle_state:
                if not GPIO.input(UP_BUTTON):  # Detect "up" button press
                    cycle_up()
                    time.sleep(0.2)  # Debounce delay
                elif not GPIO.input(DOWN_BUTTON):  # Detect "down" button press
                    cycle_down()
                    time.sleep(0.2)  # Debounce delay
                elif not GPIO.input(SELECT_BUTTON):  # Detect "select" button press
                    enter_mode()
                    time.sleep(0.2)  # Debounce delay
            else:
                # Exit mode logic is handled in individual mode functions
                pass

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    main()


