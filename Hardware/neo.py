import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Pull

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)
pixel.fill((255, 0, 255))

time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

key_home = (Keycode.COMMAND, Keycode.H)
key_screenshot = (Keycode.COMMAND, Keycode.SHIFT, Keycode.3)

key_output = key_home


def make_keystrokes(keys, delay):
    keyboard.press(*keys)
    keyboard.release_all()
    time.sleep(delay)


while True:
    if button.value and not button_state:
        pixel.fill((255, 0, 255))
        button_state = True

    if not button.value and button_state:
        pixel.fill((0, 0, 0))
        if isinstance(key_output, (list, tuple)) and isinstance(key_output[0], dict):
            for k in key_output:
                make_keystrokes(k["keys"], k["delay"])
        else:
            make_keystrokes(key_output, delay=0)
        button_state = False
