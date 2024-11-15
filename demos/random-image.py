# Imports
from PIL import Image
import zmq
import time
from evdev import InputDevice, categorize, ecodes
import requests
import io
import sys

gamepad = InputDevice("/dev/input/event1")

def exit_prog():
    print(quit)
    # canvas.delete()
    sys.exit()

# # program setup
# canvas = c.Canvas()

# Create the ZMQ connection
context = zmq.Context()

#  Socket to talk to server
#print("Connecting to LED ZMQ server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55000")


# random picture URL
w = h = 128
url = f"https://picsum.photos/{w}"

for i in range(0,3):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        # pixels = list(img.getdata())
        # print(pixels)

        # Convert the image to RGBA mode
        img = img.convert("RGBA")

        # covert to raw bytes
        rawimage = img.tobytes()

        # # send the request
        socket.send(rawimage)

        # #  Get the reply.
        message = socket.recv()

    for j in range(0,500):
        if gamepad.active_keys() == [24]:
            exit_prog()
        time.sleep(0.01)