import smbus
import time

class LCD:
    def __init__(self, i2c_address, bus_number=1):
        self.addr = i2c_address
        self.bus = smbus.SMBus(bus_number)
        self.backlight = 0x08  # Backlight ON (P3)

        time.sleep(0.05)  # LCD power-on delay

        self.write4(0x30)
        time.sleep(0.005)
        self.write4(0x30)
        time.sleep(0.001)
        self.write4(0x30)
        self.write4(0x20)  # Set to 4-bit mode

        self.command(0x28)  # Function set: 4-bit, 2 line, 5x8 dots
        self.command(0x08)  # Display off
        self.command(0x01)  # Clear display
        time.sleep(0.002)
        self.command(0x06)  # Entry mode: cursor moves right
        self.command(0x0C)  # Display on, cursor off, blink off

    def write4(self, data):
        """Send upper 4 bits to LCD with strobe"""
        self.bus_write(data & 0xF0)
        self.strobe(data & 0xF0)

    def strobe(self, data):
        self.bus_write(data | 0x04)  # EN=1
        time.sleep(0.0005)
        self.bus_write(data & ~0x04)  # EN=0
        time.sleep(0.0001)

    def bus_write(self, data):
        """Write with backlight control"""
        self.bus.write_byte(self.addr, data | self.backlight)

    def command(self, cmd):
        """Send command (RS=0)"""
        high = cmd & 0xF0
        low = (cmd << 4) & 0xF0
        self.bus_write(high)
        self.strobe(high)
        self.bus_write(low)
        self.strobe(low)

    def write_char(self, char):
        """Send data (RS=1)"""
        val = ord(char)
        high = val & 0xF0
        low = (val << 4) & 0xF0
        self.bus_write(high | 0x01)  # RS=1
        self.strobe(high | 0x01)
        self.bus_write(low | 0x01)
        self.strobe(low | 0x01)

    def set_cursor(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > 3:
            row = 3
        self.command(0x80 | (col + row_offsets[row]))

    def write(self, string, line=0, col=0):
        self.set_cursor(col, line)
        if (len(string) < 20):
            string += " " * (20 - len(string))
        for char in string:
            self.write_char(char)
