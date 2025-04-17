import smbus
import time

class LCD:
    def __init__(self, i2c_address, bus_number):
        # Initialize I2C communication
        self.i2c_address = i2c_address
        self.bus = smbus.SMBus(bus_number)
        
        # LCD configuration commands
        self.init_lcd()

    def init_lcd(self):
        # Send initialization commands to the LCD
        self.command(0x33)  # Initialize
        self.command(0x32)  # Set to 4-bit mode
        self.command(0x28)  # Set 2-line, 5x7 matrix
        self.command(0x0C)  # Turn on display, no cursor
        self.command(0x06)  # Increment cursor
        self.command(0x01)  # Clear display
        time.sleep(0.005)

    def command(self, cmd):
        # Send command to the LCD
        self.bus.write_byte(self.i2c_address, cmd)
        time.sleep(0.005)

    def write(self, string, line, side):
        # Define the starting position based on line and side
        if line == 1:
            pos = 0x80  # Line 1
        elif line == 2:
            pos = 0xC0  # Line 2
        else:
            raise ValueError("Line must be 1 or 2.")

        if side == 1:
            offset = 0  # Left side
        elif side == 2:
            offset = len(string) - 1  # Right side
        else:
            raise ValueError("Side must be 1 or 2.")

        # Move cursor to the position
        self.command(pos + offset)

        # Write the string to the LCD
        for char in string:
            self.bus.write_byte(self.i2c_address, ord(char))
            time.sleep(0.005)

# Example usage:
# Assuming LCD is connected to I2C address 0x27 and bus number 1
#lcd = LCD(i2c_address=0x27, bus_number=1)
#lcd.write("Hello!", line=1, side=1)
#lcd.write("World!", line=2, side=2)