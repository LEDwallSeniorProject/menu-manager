import time
import subprocess
import os
import sys
from threading import Thread
#from matrix_library import shapes as s, canvas as c
# from evdev import InputDevice, categorize, ecodes

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def run_program(program):
    print("Running program:", program)
    result = subprocess.run([sys.executable,program], capture_output=True, text=True)
    return result.stdout.rstrip()

def run_shutdown():
	result = subprocess.run(["/usr/bin/sudo","/usr/sbin/halt"], capture_output=True, text=True)
	return result.stdout.rstrip()

# initial setup
dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)

while True:
    # run main program
    print("Loop start - launching mainMenu")
    mainthread = ThreadWithReturnValue(target=run_program, args=("mainMenu.py",))
    mainthread.start()
    subDemo = mainthread.join()

    if subDemo == "demos":
        programs = ["demos/clock-test.py","demos/fps-test.py","demos/bounce2-test.py","demos/scrolling.py","demos/random-image.py"]

        for prog in programs:
            thread = ThreadWithReturnValue(target=run_program, args=(prog,))
            thread.start()
            result = thread.join()
            if result == "quit":
                break
    elif subDemo == "shutdown":
        thread = ThreadWithReturnValue(target=run_shutdown)
        thread.start()

    elif subDemo.startswith("game/"):
        # Extract game folder name from the printed string
        game_folder = subDemo.split("/", 1)[1]
        game_path = os.path.join(dir_path, "games", game_folder, "main.py")

        if os.path.isfile(game_path):
            # Use run_program to execute main.py in the selected game folder
            thread = ThreadWithReturnValue(target=run_program, args=(game_path,))
            thread.start()
            thread.join()
        else:
            print(f"Error: main.py not found in the folder '{game_folder}'.")

    # create a thread
    else:
        print(f"Executing {subDemo}")
        thread = ThreadWithReturnValue(target=run_program, args=(subDemo,))
        thread.start()
        thread.join()
