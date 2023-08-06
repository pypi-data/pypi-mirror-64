import gpiodcxx
import sys
import time
from datetime import timedelta

try:
    if len(sys.argv) > 2:
        BUTTON_CHIP = sys.argv[1]
        BUTTON_LINE_OFFSET = int(sys.argv[2])
        if len(sys.argv) > 3:
            edge = sys.argv[3]
            if edge[0] == 'r':
                BUTTON_EDGE = gpiodcxx.line_request.EVENT_RISING_EDGE
            elif edge[0] == 'f':
                BUTTON_EDGE = gpiodcxx.line_request.EVENT_FALLING_EDGE
            else:
                BUTTON_EDGE = gpiodcxx.line_request.EVENT_BOTH_EDGES
        else:
            BUTTON_EDGE = gpiodcxx.line_request.EVENT_BOTH_EDGES

    else:
        raise
except:
    print('''Usage:
    python3 -m gpiodcxx.test.button <chip> <line offset> [rising|falling|both]''')
    sys.exit()

chip = gpiodcxx.chip(BUTTON_CHIP)
button = chip.get_line(BUTTON_LINE_OFFSET)

config = gpiodcxx.line_request()
config.consumer = "Button"
config.request_type = BUTTON_EDGE

button.request(config)

while True:
    if button.event_wait(timedelta(minutes=1)):
        # event_read() is blocking function.
        event = button.event_read()
        if event.event_type == gpiodcxx.line_event.RISING_EDGE:
            print("rising")
        else:
            print("falling")
