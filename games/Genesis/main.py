from matrix_library import shapes as s, canvas as c
from evdev import InputDevice, categorize, ecodes

canvas = c.Canvas()

gamepad = InputDevice("/dev/input/event1")


def exit_prog():
    print("quit")
    canvas.delete()
    sys.exit()


text = s.Phrase(
    "In the beginning, God created the heavens and the earth. The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters. And God said, 'Let there be light,' and there was light. And God saw that the light was good. And God separated the light from the darkness. God called the light Day, and the darkness he called Night. And there was evening and there was morning, the first day. And God said, 'Let there be an expanse in the midst of the waters, and let it separate the waters from the waters.' And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so. And God called the expanse Heaven. And there was evening and there was morning, the second day.",
    [0, 0],
    auto_newline=True,
)

for i in range(400):
    if gamepad.active_keys() == [24]:
        exit_prog()

    canvas.clear()
    text.translate(0, -1)
    canvas.add(text)
    canvas.draw()