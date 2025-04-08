import RPi.GPIO as GPIO
import threading

class EncoderReader:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b

        self.count_a = 0
        self.count_b = 0
        self.lock = threading.Lock()
        self.running = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _callback_a(self, channel):
        with self.lock:
            self.count_a += 1

    def _callback_b(self, channel):
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
