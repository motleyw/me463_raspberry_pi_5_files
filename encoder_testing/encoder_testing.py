from component_modules.encoder_class import Encoder

encoder = Encoder(pin_a=21, pin_b=22)
#encoder = Encoder(pin_a=23, pin_b=24)
encoder.start()

try:
    while True:
        print(encoder.speed())
except KeyboardInterrupt:
    print("\nExiting...")

finally:
    encoder.stop()