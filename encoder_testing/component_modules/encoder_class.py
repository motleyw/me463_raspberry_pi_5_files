import RPi.GPIO as GPIO
import threading
import time

class Encoder:
    def __init__(self, pin_a, pin_b, debounce_ms=20):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.debounce_ms = debounce_ms

        self.count_a = 0
        self.count_b = 0

        self.last_time_a = 0
        self.last_time_b = 0

        self.angular_velocity = 0

        self.lock = threading.Lock()
        self.running = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _callback_a(self, channel):
        now = time.time() * 1000
        if now - self.last_time_a > self.debounce_ms:
            self.last_time_a = now
            with self.lock:
                self.count_a += 1

    def _callback_b(self, channel):
        now = time.time() * 1000
        if now - self.last_time_b > self.debounce_ms:
            self.last_time_b = now
            with self.lock:
                self.count_b += 1

    def start(self):
        if not self.running:
            GPIO.add_event_detect(self.pin_a, GPIO.RISING, callback=self._callback_a)
            GPIO.add_event_detect(self.pin_b, GPIO.RISING, callback=self._callback_b)
            self.running = True

    def stop(self):
        if self.running:
            GPIO.remove_event_detect(self.pin_a)
            GPIO.remove_event_detect(self.pin_b)
            self.running = False

    def get_counts(self):
        with self.lock:
            return self.count_a, self.count_b
