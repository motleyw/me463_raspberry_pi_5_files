from component_modules.encoder_class import Encoder

#encoder = Encoder(pin_a=21, pin_b=22, debounce_ms=10)
encoder = Encoder(pin_a=23, pin_b=24, debounce_ms=10)
encoder.start()

try:
    while True:
        print(encoder.get_counts())
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    encoder.stop()