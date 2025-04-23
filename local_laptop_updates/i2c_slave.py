from machine import Pin
import rp2

@rp2.asm_pio(
    in_shiftdir=rp2.PIO.SHIFT_LEFT,
    pull_thresh=8,
    autopull=True,
    sideset_init=(rp2.PIO.OUT_HIGH,)
)
def i2c_slave_rx():
    wrap_target()
    wait(0, pin, 1)
    wait(1, pin, 0)
    set(x, 7)
    label("bitloop")
    wait(1, pin, 1)
    in_(pins, 1)
    wait(0, pin, 1)
    jmp(x_dec, "bitloop")
    push(block)
    wrap()

@rp2.asm_pio(
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopush=True,
    push_thresh=8,
    sideset_init=(rp2.PIO.OUT_HIGH,)
)
def i2c_slave_tx():
    wrap_target()
    pull()
    set(x, 7)
    label("bitloop")
    out(pins, 1)
    wait(1, pin, 1)
    wait(0, pin, 1)
    jmp(x_dec, "bitloop")
    wrap()

class I2CSlave:
    def __init__(self, sm_rx=0, sm_tx=1, scl=1, sda=0, addr=0x42):
        self.addr = addr
        self.sda_pin = Pin(sda, Pin.IN, Pin.PULL_UP)
        self.scl_pin = Pin(scl, Pin.IN, Pin.PULL_UP)

        self.sm_rx = rp2.StateMachine(sm_rx, i2c_slave_rx, freq=100_000,
                                      in_base=self.sda_pin, sideset_base=self.scl_pin)
        self.sm_tx = rp2.StateMachine(sm_tx, i2c_slave_tx, freq=100_000,
                                      out_base=self.sda_pin, sideset_base=self.scl_pin)

        self.sm_rx.active(1)
        self.sm_tx.active(1)

    def write(self, val):
        self.sm_tx.put(val)
