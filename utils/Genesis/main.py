import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

text = matrix.Phrase(
    "In the beginning, God created the heavens and the earth. The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters. And God said, 'Let there be light,' and there was light. And God saw that the light was good. And God separated the light from the darkness. God called the light Day, and the darkness he called Night. And there was evening and there was morning, the first day. And God said, 'Let there be an expanse in the midst of the waters, and let it separate the waters from the waters.' And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so. And God called the expanse Heaven. And there was evening and there was morning, the second day.",
    [0, 0],
    auto_newline=True,
)

controller.add_function("START", exit_prog)

for i in range(400):
    if exited: sys.exit(0)
    canvas.clear()
    text.translate(0, -1)
    canvas.add(text)
    canvas.draw()
