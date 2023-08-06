import gpiodcxx
import sys
import time

try:
    if len(sys.argv) > 2:
        LED_CHIP = sys.argv[1]
        LED_LINE_OFFSETS = []
        for i in range(len(sys.argv) - 2):
            LED_LINE_OFFSETS.append(int(sys.argv[i+2]))
    else:
        raise
except:
    print('''Usage:
    python3 -m gpiodcxx.test.blinks <chip> <line offset1> [<line offset2> ...]''')
    sys.exit()

chip = gpiodcxx.chip(LED_CHIP)
leds = chip.get_lines(LED_LINE_OFFSETS)

config = gpiodcxx.line_request()
config.consumer = "Blink"
config.request_type = gpiodcxx.line_request.DIRECTION_OUTPUT

leds.request(config)

off = [0] * leds.size()
on = [1] * leds.size()

while True:
    leds.set_values(off)
    time.sleep(0.1)
    leds.set_values(on)
    time.sleep(0.1)
