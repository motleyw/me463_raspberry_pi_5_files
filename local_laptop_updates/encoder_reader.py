import RPi.GPIO as GPIO
import threading
import time

class Encoder:
    def __init__(self, pin_a, pin_b, interval=0.1):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.interval = interval
        self.pulse_count_a = 0
        self.pulse_count_b = 0
        self.speed = 0.0
        self.running = False
        self.lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin_a, GPIO.RISING, callback=self._pulse_callback)

    def _pulse_callback_a(self, channel):
        with self.lock:
            self.pulse_count_a += 1

    def _pulse_callback_b(self, channel):
        with self.lock:
            self.pulse_count_b += 1 

    def _measure_loop(self):
        while self.running:
            time.sleep(self.interval)
            with self.lock:
                count = self.pulse_count
                self.pulse_count = 0
            self.speed = count / self.interval  # pulses per second

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._measure_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        GPIO.remove_event_detect(self.pin_a)

    def get_speed(self):
        return self.speed
