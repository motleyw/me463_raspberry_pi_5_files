from lcd_class import LCD  # Assuming your class is saved in lcd.py
import time

if __name__ == "__main__":
    lcd = LCD(i2c_address=0x27, bus_number=2)  # Use your I²C address and bus

    lcd.write("Hello, world!", line=0)
    lcd.write("Line 2 text", line=1)
    lcd.write("Line 3 text", line=2)
    lcd.write("Line 4 text", line=3)
