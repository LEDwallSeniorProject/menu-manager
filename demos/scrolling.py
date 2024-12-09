from matrix_library import canvas as c, shapes as s
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice("/dev/input/event1")

canvas = c.Canvas()

text = s.Phrase("Welcome to Calvin!", [32, 64], size=6)

def exit_prog():
    print(quit)
    canvas.delete()
    sys.exit()

counter = 0
while counter <= 450:
    if gamepad.active_keys() == [24]:
        exit_prog()

    canvas.clear()
    text.translate(-2, 0)
    if text.get_width() + text.position[0] < 0:
        text.set_position([128, (text.position[1] + 64) % 128])
    canvas.add(text)
    canvas.draw()

    counter += 1