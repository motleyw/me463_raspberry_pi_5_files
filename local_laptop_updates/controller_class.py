# This class is used to control the motor speed using PWM signals.
# The main method is calc_PWM which takes an error value computed from input and measured motor speed and calculated a PWM output value
# The coefficients are in the order: [Proportional (Kp), Integral(Ki), Derivative(Kd)]

class Controller:
    def __init__(self, coefficients, type="PID"):
        self.coefficients = coefficients
        self.previous_error = 0.0
        self.sum_error = 0.0


    def calculate_pwm(self, error, dt):
        if (type == "PID"):
            PWM = 0

            # Calculate Proportional Gain
            p = self.coefficients[0] * error

            # Calculate Integral Gain
            self.sum_error += error * dt
            i = self.coefficients[1] * self.sum_error

            # Calculate Derivative Gain
            d = self.coefficients[2] * (error - self.previous_error) / dt

            self.previous_error = error

            PWM = p + i + d

            #Scaling here! Might need adjustments!!!
            if PWM > 100:
                PWM = 100
            elif PWM < 0:
                PWM = 0

            return PWM
        elif (type == "FF"):
            # Calculate Feed Forward Gain
            FF = self.coefficients[0] * error

            #Scaling here! Might need adjustments!!!
            if FF > 100:
                FF = 100
            elif FF < 0:
                FF = 0

            return FF
        else:
            raise ValueError("Invalid controller type. Use 'PID' or 'FF'.")
    

    
 