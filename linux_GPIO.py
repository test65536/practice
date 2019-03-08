import gpio
import time
gpio.cleanup(63)  # 15-63
while True:
    gpio.setup(63, 'out')
    gpio.set(63, 1)
    time.sleep(1)
    gpio.set(63, 0)
    time.sleep(1)
