import string
import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False
alphabet = ''

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

controller.add_function("START", exit_prog)

for i in string.ascii_lowercase:
    if exited: sys.exit(0)
    alphabet += i
    test = matrix.Phrase(
        alphabet,
        (0, 0),
        (255, 255, 255),
        auto_newline=True,
        size=1,
    )

    canvas.clear()
    canvas.add(test)
    canvas.draw()
    time.sleep(0.3)
