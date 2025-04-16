# This class is used to control the motor speed using PWM signals.
# The main method is calc_PWM which takes an error value computed from input and measured motor speed and calculated a PWM output value

class Controller:
    def __init__(self, coefficients):
        self.coefficients = coefficients


    def calculate_pwm(self, error):
        PWM = 0
        p = self.coefficients[0] * error
        #Scaling here
        return PWM
 