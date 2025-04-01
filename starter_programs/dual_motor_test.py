import RPi.GPIO as GPIO
import time

class DualMotorDriver:
    def __init__(self, motor1_pins, motor2_pins, frequency=1000):
        GPIO.setmode(GPIO.BCM)
        
        self.motors = {
            "motor1": {"in1": motor1_pins[0], "in2": motor1_pins[1]},
            "motor2": {"in1": motor2_pins[0], "in2": motor2_pins[1]}
        }
        
        for motor in self.motors.values():
            GPIO.setup(motor["in1"], GPIO.OUT)
            GPIO.setup(motor["in2"], GPIO.OUT)
            
        self.pwm = {
            "motor1": {"in1": GPIO.PWM(self.motors["motor1"]["in1"], frequency),
                        "in2": GPIO.PWM(self.motors["motor1"]["in2"], frequency)},
            "motor2": {"in1": GPIO.PWM(self.motors["motor2"]["in1"], frequency),
                        "in2": GPIO.PWM(self.motors["motor2"]["in2"], frequency)}
        }
        
        for motor in self.pwm.values():
            motor["in1"].start(0)
            motor["in2"].start(0)

    def set_motor_speed(self, motor, speed):
        """Set speed and direction for the motor (-100 to 100)"""
        if motor not in self.motors:
            raise ValueError("Invalid motor selection. Choose 'motor1' or 'motor2'")
        
        speed = max(-100, min(100, speed))  # Constrain speed to -100 to 100
        duty_cycle = abs(speed)
        
        if speed > 0:
            self.pwm[motor]["in1"].ChangeDutyCycle(duty_cycle)
            self.pwm[motor]["in2"].ChangeDutyCycle(0)
        elif speed < 0:
            self.pwm[motor]["in1"].ChangeDutyCycle(0)
            self.pwm[motor]["in2"].ChangeDutyCycle(duty_cycle)
        else:
            self.pwm[motor]["in1"].ChangeDutyCycle(0)
            self.pwm[motor]["in2"].ChangeDutyCycle(0)
    
    def stop(self):
        for motor in self.pwm.values():
            motor["in1"].ChangeDutyCycle(0)
            motor["in2"].ChangeDutyCycle(0)
        
    def cleanup(self):
        self.stop()
        GPIO.cleanup()

# Example Usage
if __name__ == "__main__":
    motor_driver = DualMotorDriver(motor1_pins=(12, 13), motor2_pins=(18, 20))
    try:
        for i in range(0, 50):
            motor_driver.set_motor_speed("motor1", -i)  # Forward at 50% speed
            motor_driver.set_motor_speed("motor2", i) # Reverse at 50% speed
            time.sleep(0.1)
        time.sleep(3)
        motor_driver.stop()
    except KeyboardInterrupt:
        motor_driver.cleanup()
    finally:
        motor_driver.cleanup()
