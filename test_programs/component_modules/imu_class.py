import smbus
import time
import RPi.GPIO as GPIO
import threading

class IMU:
    def __init__(self, sampling_time=0.01, bus=0, addr=0x68):
        self.i2c_bus = smbus.SMBus(bus)
        self.device_addr = addr
        self.registers = {"x_l": 0x3B, "y_l": 0x3D, "z_l": 0x3F, "x_r": 0x43, "y_r": 0x45, "z_r": 0x47}  # _l is linear, _r is rotation
        self.acceleration = {"x_l": 0, "y_l": 0, "z_l": 0, "x_r": 0, "y_r": 0, "z_r": 0}
        self.velocity = {"x_l": 0, "y_l": 0, "z_l": 0, "x_r": 0, "y_r": 0, "z_r": 0}
        self.position = {"x_l": 0, "y_l": 0, "z_l": 0, "x_r": 0, "y_r": 0, "z_r": 0}
        self.sampling_time = sampling_time

        self.lock = threading.Lock()
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None

    def read_data(self, reg):
        high = self.i2c_bus.read_byte_data(self.device_addr, reg)
        low = self.i2c_bus.read_byte_data(self.device_addr, reg + 1)
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value
    
    def get_acceleration(self):
        for key in self.registers:
            with self.lock:
                self.acceleration[key] = self.read_data(self.registers[key])

    def _data_updater(self):
        while not self.stop_event.is_set:
            with self.lock:
                self.get_acceleration()
            time.sleep(self.sampling_time)

    def start(self):
        if not self.running:
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._speed_updater, daemon=True)
            self.thread.start()
            self.running = True
            
    def stop(self):
        if self.running:
            self.stop_event.set()
            self.running = False
    
    def display_acceleration(self):
        with self.lock:
            print(self.acceleration)
    
    def get_acceleration(self):
        with self.lock:
            return self.acceleration
