import pygame
from dual_motor_test import DualMotorDriver

motor_driver = DualMotorDriver(motor1_pins=(12, 13), motor2_pins=(18, 20))

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

# Main event loop
try:
    while True:
        pygame.event.pump()  # Process events
        
        # Check for button presses
        for button_id in range(controller.get_numbuttons()):
            if controller.get_button(button_id):
                print(f"Button {button_map.get(button_id, 'Unknown')} pressed")

        # Check for joystick movement
        left_x = controller.get_axis(0)
        left_y = controller.get_axis(1)
        right_x = controller.get_axis(2)
        right_y = controller.get_axis(3)

        if abs(left_x) > 0.1 or abs(left_y) > 0.1:
            print(f"Left Joystick: X={left_x:.2f}, Y={left_y:.2f}")

        if abs(right_x) > 0.1 or abs(right_y) > 0.1:
            print(f"Right Joystick: X={right_x:.2f}, Y={right_y:.2f}")

        motor_driver.set_motor_speed("motor1", int(left_y * 20))  # Forward at 50% speed
        motor_driver.set_motor_speed("motor2", int(right_y * 20)) # Reverse at 50% speed

        pygame.time.wait(100)  # Delay to avoid excessive CPU usage

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    pygame.joystick.quit()
    pygame.quit()
