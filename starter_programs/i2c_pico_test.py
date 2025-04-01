import smbus2
import time

# Define the I2C bus and slave address
I2C_BUS = 3  # Raspberry Pi 5 uses I2C bus 1
SLAVE_ADDR = 0x42  # Slave address (must match the address used in the slave script)

# Create I2C bus object
bus = smbus2.SMBus(I2C_BUS)

def write_to_slave(data):
    try:
        # Write data to slave
        bus.write_i2c_block_data(SLAVE_ADDR, 0, list(data))  # 0 is the command, change if needed
        print(f"Sent to slave: {data}")
    except Exception as e:
        print(f"Error writing to slave: {e}")

def read_from_slave():
    try:
        # Read data from slave
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, 32)  # 32 is the max number of bytes to read
        print(f"Received from slave: {bytes(data)}")
        return bytes(data)
    except Exception as e:
        print(f"Error reading from slave: {e}")

while True:
    # Write data to slave
    write_to_slave(b"Hello, Pi Pico!")
    
    # Give the slave time to process and respond
    time.sleep(1)
    
    # Read data from slave
    read_from_slave()
    
    # Wait before next communication
    time.sleep(2)
