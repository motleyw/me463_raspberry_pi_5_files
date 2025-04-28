import RPi.GPIO as GPIO
import threading
import time

class Encoder:
    def __init__(self, pin_a, pin_b, debounce_s=0.00, rads_per_count=0.06, update_interval=0.005):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.debounce_s = debounce_s  # sec
        self.rads_per_count = rads_per_count
        self.update_interval = update_interval

        self.count_a = 0
        self.count_b = 0

        self.last_time_a = 0  # sec
        self.last_time_b = 0  # sec
        self.last_count_a = 0  # sec
        self.last_count_b = 0  # sec

        self.direction = 1
        self.angular_velocity = 0

        self.lock = threading.Lock()
        self.running = False
        self.updater_thread = None
        self.stop_event = threading.Event()

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _callback_a(self, channel):
        now = time.time()
        if now - self.last_time_a > self.debounce_s:
            self.dt_a = now - self.last_time_a
            self.last_time_a = now
            with self.lock:
                self.count_a += 1
                if GPIO.input(self.pin_b) == GPIO.HIGH:
                    self.direction = 1
                else:
                    self.direciton = -1

    def _callback_b(self, channel):
        now = time.time()
        if now - self.last_time_b > self.debounce_s:
            self.dt_b = now - self.last_time_b
            self.last_time_b = now
            with self.lock:
                self.count_b += 1
                if GPIO.input(self.pin_a) == GPIO.HIGH:
                    self.direction = -1
                else:
                    self.direciton = 1

    def _speed_updater(self):
        while not self.stop_event.is_set():
            with self.lock:
                dc_a = self.count_a - self.last_count_a
                dc_b = self.count_b - self.last_count_b
                self.angular_velocity = self.direction * self.rads_per_count * ((dc_a / self.update_interval + dc_b / self.update_interval) / 2)
                self.last_count_a = self.count_a
                self.last_count_b = self.count_b
            time.sleep(self.update_interval)

    def start(self):
        if not self.running:
            GPIO.add_event_detect(self.pin_a, GPIO.RISING, callback=self._callback_a)
            GPIO.add_event_detect(self.pin_b, GPIO.RISING, callback=self._callback_b)
            self.stop_event.clear()
            self.updater_thread = threading.Thread(target=self._speed_updater, daemon=True)
            self.updater_thread.start()
            self.running = True

    def stop(self):
        if self.running:
            GPIO.remove_event_detect(self.pin_a)
            GPIO.remove_event_detect(self.pin_b)
            self.running = False

    def get_counts(self):
        with self.lock:
            return self.count_a, self.count_b

    def speed(self):
        with self.lock:
            return self.angular_velocity
