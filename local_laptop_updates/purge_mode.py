# This script is designed to be the purging system for the robot (to clear out particulate)

import RPi.GPIO as GPIO
import time
from encoder_class import Encoder
from motor_class import Motor
from controller_class import Controller

def purge_mode():
    # Start encoder monitoring
    left_encoder = Encoder(pin_a=21, pin_b=22)
    right_encoder = Encoder(pin_a=23, pin_b=24)
    left_encoder.start()
    right_encoder.start()

    left_motor = Motor(pins={"forward": 13, "backward": 12}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=left_encoder, pwm_frequency=1000, min=20)
    right_motor = Motor(pins={"forward": 18, "backward": 20}, set_speed=0, coefficients=[6.8235, 0.1836], c_type="FF_1", encoder=right_encoder, pwm_frequency=1000, min=20)

    drum_motor = Motor({"forward":19}, set_speed=0, coefficients=[-6.9932, 4.4445, -343.31, 32.46], c_type="FF_2", encoder=None, pwm_frequency=1000, min=20)
    flywheel_motor = Motor({"forward":17}, set_speed=0, coefficients=[3.8739, 0.1569], c_type="FF_1", encoder=None, pwm_frequency=1000, min=32)

    SELECT_BUTTON = 5    # GPIO pin for the "select" button
    LIMIT_SWITCH = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SELECT_BUTTON, GPIO.IN)
    GPIO.setup(LIMIT_SWITCH, GPIO.IN)

    # Initialize pygame's joystick module
    pygame.init()
    pygame.joystick.init()

    # Detect and initialize the first available controller
    if pygame.joystick.get_count() == 0:
        print("No controllers detected. Make sure your Xbox controller is connected via Bluetooth.")
        exit()

    controller = pygame.joystick.Joystick(0)
    controller.init()

    print(f"Connected to: {controller.get_name()}")

    # Define button mappings
    button_map = {
        0: "A",
        1: "B",
        2: "X",
        3: "Y",
        4: "LB",
        5: "RB",
        6: "Back",
        7: "Start",
        8: "Xbox",
        9: "Left Stick",
        10: "Right Stick"
    }

    toggle = False

    # Main event loop
    try:
        stop_toggle = False
        while not toggle:
            pygame.event.pump()  # Process events

            # Check for button presses
            for button_id in range(controller.get_numbuttons()):
                if controller.get_button(button_id):
                    print(f"Button {button_map.get(button_id, 'Unknown')} pressed")

            # Check for joystick movement
            left_x = controller.get_axis(0)
            left_y = -controller.get_axis(1)
            right_x = controller.get_axis(2)
            right_y = -controller.get_axis(3)

            if abs(left_x) > 0.1 or abs(left_y) > 0.1:
                print(f"Left Joystick: X={left_x:.2f}, Y={left_y:.2f}")

            if abs(right_x) > 0.1 or abs(right_y) > 0.1:
                print(f"Right Joystick: X={right_x:.2f}, Y={right_y:.2f}")

            if (stop_toggle == False) & (GPIO.input(LIMIT_SWITCH) == GPIO.LOW):  # E-stop not activated

                # Set motor speeds based on joystick input
                left_speed = int(left_y * 25)
                right_speed = int(left_y * 25)
                turning_speed = int(left_x * 15) # If PWM is 100, motors stop

                stimput = ((left_y)**2 + (left_x)**2)**(1/2)
                print(stimput)
                if stimput > 0.5:
                    left_motor.PWM = (left_speed + turning_speed)
                    right_motor.PWM = (right_speed - turning_speed)
                else:
                    print(stimput)
                    left_motor.PWM = 0
                    right_motor.PWM = 0
                    left_motor.stop_motor()
                    right_motor.stop_motor()
                print(f"Left PWM: {left_motor.PWM}, Right PWM: {right_motor.PWM}")

                left_motor.set_motor_speed()
                right_motor.set_motor_speed()
                
                #if the right trigger is pressed, set the drum motor speed
                if controller.get_button(5):
                    drum_motor.PWM = int(right_y * 50 + 50)
                    drum_motor.set_motor_speed()
                else:
                    drum_motor.PWM = 0
                    drum_motor.set_motor_speed()
                
                #if the left trigger is pressed, set the flywheel motor speed
                if controller.get_button(4):
                    flywheel_motor.PWM = int(80)
                    flywheel_motor.set_motor_speed() # Set to 80% speed for flywheel
                else:
                    flywheel_motor.PWM = 0
                    flywheel_motor.set_motor_speed()

                if controller.get_button(3):
                    stop_toggle = True
                    time.sleep(0.1)
                    print("E-stop activated. Press Y button to deactivate.")

            elif (stop_toggle == True) or (GPIO.input(LIMIT_SWITCH) != GPIO.LOW):
                # E-stop activated, stop all motors
                left_motor.stop_motor()
                right_motor.stop_motor()
                drum_motor.PWM = 0
                drum_motor.set_motor_speed()
                flywheel_motor.PWM = 0
                flywheel_motor.set_motor_speed()
                print(stop_toggle)

                if controller.get_button(3):
                    stop_toggle = not stop_toggle
                    time.sleep(0.1)
                    print("E-stop deactivated.")

            if GPIO.input(SELECT_BUTTON) == GPIO.LOW:
                toggle = True
                print("Exiting BTC mode...")
                time.sleep(0.2)

            pygame.time.wait(100)  # Delay to avoid excessive CPU usage

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        pygame.joystick.quit()
        pygame.quit()
        right_encoder.stop()
        left_encoder.stop()
        left_motor.stop_motor()
        right_motor.stop_motor()
        drum_motor.stop_motor()
        flywheel_motor.stop_motor()
        left_motor.cleanup()
        right_motor.cleanup()
        drum_motor.cleanup()
        flywheel_motor.cleanup()
