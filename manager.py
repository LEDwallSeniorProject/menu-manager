from matrix_library import LEDWall, Canvas, Controller, shapes
from os import scandir, chdir, getcwd, path
from importlib.util import spec_from_file_location, module_from_spec
import shutil
import subprocess
import time

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
TITLECOLOR = (50, 255, 50)
ERRORCOLOR = (255, 80, 80)

class MainMenu(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        # pointer to subclass to be executed on loop halt
        self.queued = None

        # options to select / current selection
        self.selection = 0
        self.options = []

        # track SELECT hold timing for safe shutdown
        self._stop_hold_threshold = 3.0
        self._stop_hold_reset_gap = 0.25
        self._stop_states = {
            "SELECT": {"start": None, "last": None},
            "SELECT2": {"start": None, "last": None},
        }
        self._shutdown_triggered = False
        
        # begin the code
        super().__init__(canvas, controller, trackFPS=False, fps=15)

    def preLoop(self):
        self.autoRunTime = time.time()

        # set the path to start the menu at and get the options within
        self.base_path = path.dirname(path.abspath(__file__))
        chdir(self.base_path)
        self.getOptions()

    def postLoop(self):
        if self.queued != None:
            try:
                self.queued(self.canvas, self.controller)
            except Exception as e:
                raise RuntimeError("Error occured running the selected program, within the selected program. ") from e

        if not self.__exited__:
            self.__init__(self.canvas, self.controller)
        elif self._shutdown_triggered:
            return
        else:
            self.canvas.clear()
            self.canvas.add(shapes.Phrase("GOODBYE", (0, 5), TITLECOLOR, size=1.5))
            self.canvas.draw()
            time.sleep(2)
            self.canvas.clear()

    def __draw__(self):
        title = shapes.Phrase("MENU", (64, 5), TITLECOLOR, size=1.5)
        title.translate(0 - title.get_width() / 2, 0)
        self.canvas.add(title)

        for index, item in enumerate(self.options):
            itemColor = WHITE if self.selection != index else BLUE
            option = shapes.Phrase(
                item,
                (64, 32 + index * 12),
                itemColor,
            )
            option.translate(0 - option.get_width() / 2, 0)
            self.canvas.add(option)

        # if (time.time() - self.autoRunTime) > 12:
        #     self.autoRunner()

    def __bind_controls__(self):
        self.controller.add_function("LB", self.toggle_track_fps)
        self.controller.add_function("UP", self.selection_up)
        self.controller.add_function("DOWN", self.selection_down)
        self.controller.add_function("A", self.enter)
        self.controller.add_function("Y", self.enter)
        self.controller.add_function("START", self.enter)
        self.controller.add_function("SELECT", self._select_stop)
        self.controller.add_function("UP2", self.selection_up)
        self.controller.add_function("DOWN2", self.selection_down)
        self.controller.add_function("A2", self.enter)
        self.controller.add_function("Y2", self.enter)
        self.controller.add_function("START2", self.enter)
        self.controller.add_function("SELECT2", self._select2_stop)

    def toggle_track_fps(self):
        self.trackFPS = not self.trackFPS

    def selection_up(self):
        self.selection = (self.selection - 1) % len(self.options)
        self.autoRunTime = time.time()

    def selection_down(self):
        self.selection = (self.selection + 1) % len(self.options)
        self.autoRunTime = time.time()

    def enter(self):
        if self.options[self.selection] == "Exit":
            self._trigger_shutdown()
            return

        elif self.options[self.selection] == "Back":
            chdir("..")
            self.options = []
            self.getOptions()

        else:
            chdir(self.options[self.selection])
            self.checkExecutable()
            self.options = []
            self.getOptions()
        
        self.autoRunTime = time.time()

    def checkExecutable(self):
        try:
            with scandir() as directory:
                for handle in directory:
                    moduleName = f"{path.basename(getcwd())}"
                    moduleName = moduleName[0].upper() + moduleName[1:]
                    if (
                        not handle.name.startswith(".")
                        and handle.is_file()
                        and handle.name == moduleName + ".py"
                    ):
                        # dynamically import the module safely based on the absolute path
                        moduleSpec = spec_from_file_location(
                            moduleName, f"{getcwd()}/{moduleName}.py"
                        )
                        module = module_from_spec(moduleSpec)
                        moduleSpec.loader.exec_module(module)

                        # queue for execution and stop the loop
                        # specifically, load class from module and set it to queue pointer
                        self.queued = getattr(module, moduleName)
                        self.running = False

        except Exception as e:
            print(
                "Something went wrong trying to look for or execute that program. Error:\n",
                e,
            )
            # traverse back one
            chdir("..")
            self.options = []
            self.getOptions()

    def getOptions(self):
        try:
            with scandir() as directory:
                for handle in directory:
                    if (
                        not handle.name.startswith(".")
                        and not handle.name.startswith("__")
                        and handle.is_dir()
                    ):
                        self.options.append(handle.name)

        except Exception as e:
            raise Exception(
                "Something went wrong trying to look for options in the current directory"
            ) from e

        self.options.sort()
        if self.isBasePath() == False:
            self.options.append("Back")
        else:
            self.options.append("Exit")

    def isBasePath(self):
        return path.abspath(getcwd()) == path.abspath(self.base_path)

    def _select_stop(self):
        self._handle_stop_hold("SELECT")

    def _select2_stop(self):
        self._handle_stop_hold("SELECT2")

    def _handle_stop_hold(self, button):
        now = time.time()
        state = self._stop_states[button]

        if (
            state["start"] is None
            or state["last"] is None
            or (now - state["last"]) > self._stop_hold_reset_gap
        ):
            state["start"] = now

        state["last"] = now

        if state["start"] is not None and (now - state["start"]) >= self._stop_hold_threshold:
            self._trigger_shutdown()

    def _reset_stop_states(self):
        for state in self._stop_states.values():
            state["start"] = None
            state["last"] = None

    def __stop__(self):
        self._reset_stop_states()
        super().__stop__()

    def _trigger_shutdown(self):
        if self._shutdown_triggered:
            return

        self._shutdown_triggered = True
        self._show_shutdown_message()
        if self._shutdown_system():
            self.__stop__()
        else:
            self._shutdown_triggered = False
            self._reset_stop_states()

    def _show_shutdown_message(self):
        self._show_centered_phrase("SHUTDOWN", TITLECOLOR, 2)

    def _show_shutdown_error(self, detail):
        print(f"Failed to initiate system shutdown: {detail}")
        self._show_centered_phrase("SHUTDOWN FAILED", ERRORCOLOR, 2)

    def _show_centered_phrase(self, text, color, seconds):
        self.canvas.clear()
        phrase = shapes.Phrase(text, (64, 40), color, size=1.5)
        phrase.translate(0 - phrase.get_width() / 2, 0)
        self.canvas.add(phrase)
        self.canvas.draw()
        time.sleep(seconds)
        self.canvas.clear()
        self.canvas.draw()

    def _shutdown_system(self):
        sudo_path = shutil.which("sudo") or "sudo"

        try:
            subprocess.Popen(
                [sudo_path, "shutdown", "-h", "now"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            self._show_shutdown_error(str(e))
            return False

        return True

if __name__ == "__main__":
    canvas = Canvas(limitFps=False)

    if canvas.render == "zmq":
        img = shapes.Image(width=128, height=128, position=[0,0])
        img.loadfile(filename="startup.png")
        canvas.add(img)
        canvas.draw()
        time.sleep(1)
    
    controller = Controller()
    MainMenu(canvas,controller)
