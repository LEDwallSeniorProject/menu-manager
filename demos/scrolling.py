import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False
text = matrix.Phrase("Welcome to Calvin!", [32, 64], size=6)

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

controller.add_function("START", exit_prog)

counter = 0
while counter <= 450:

    # check if exited
    if exited: sys.exit(0)

    canvas.clear()
    text.translate(-2, 0)
    if text.get_width() + text.position[0] < 0:
        text.set_position([128, (text.position[1] + 64) % 128])
    canvas.add(text)
    canvas.draw()

    counter += 1