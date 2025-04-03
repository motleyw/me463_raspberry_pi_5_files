import serial

ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
ser.write(b"$PUBX,41,1,0007,0003,9600,0*14\r\n")  # Switch to NMEA at 9600 baud
ser.close()