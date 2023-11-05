from pynput import keyboard
from PIL import ImageGrab
import pytesseract
import time

monkeytype_dims = (150, 525, 1700, 700)
monkeytype_half_dims = (150, 375, 1700, 550)
keybr_comp_dims = (150, 600, 1600, 750)
keybr_practice_dims = (150, 400, 1600, 550)
monkeytype_lang_dims = (175, 340, 260, 380)
should_i_type = True
dont_stop_typing = True

keyboard_output = keyboard.Controller()

SPEED_109 = 0.1
SPEED_213 = 0.045
SPEED_769 = 0.009
SPEED_INF = 0

DELAY = SPEED_INF

ocr_string = ""


def on_activate():
    global dont_stop_typing
    global should_i_type
    dont_stop_typing = False
    should_i_type = False
    print('Execution stopped')


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('`'),
    on_activate)

listener = keyboard.Listener(
    on_press=for_canonical(hotkey.press),
    on_release=for_canonical(hotkey.release))
listener.start()

time.sleep(2)
img = ImageGrab.grab(bbox=monkeytype_lang_dims)

print(pytesseract.image_to_string(
    img))
img.save(f"lang_sgrab.png")

iter = 0
while dont_stop_typing:
    iter += 1
    time.sleep(0.2)
    img = ImageGrab.grab(bbox=monkeytype_dims)

    print(img)
    img.save(f"screengrab{iter}.png")

    new_ocr_string = repr(pytesseract.image_to_string(
        img)).replace(r'\n', ' ').replace("'", '')

    print("scans: ", ocr_string, "\n\n", new_ocr_string, len(new_ocr_string))

    if (new_ocr_string.find("raw") != -1 and new_ocr_string.find("characters") != -1) or len(new_ocr_string) < 30:
        print("test complete")
        dont_stop_typing = False
        should_i_type = False

    elif ocr_string.find(new_ocr_string[:20]) != -1 and new_ocr_string != ocr_string:
        print("new test found")
        last_word_index = new_ocr_string.find(ocr_string[-20:]) + 20
        ocr_string = new_ocr_string[last_word_index:]
    else:
        print("test started")
        ocr_string = new_ocr_string

    print("")
    print(ocr_string)

    # if should_i_type:

    for i in ocr_string:
        if not should_i_type: break
        time.sleep(DELAY)
        keyboard_output.type(i)
