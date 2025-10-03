from matrix_library import LEDWall, Canvas, Controller, shapes
from os import scandir, chdir, getcwd, path
from importlib.util import spec_from_file_location, module_from_spec
import shutil
import subprocess
import threading
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
        self.hidden_dirs = {"test"}

        # track SELECT hold timing for safe shutdown
        self._stop_hold_threshold = 3.0
        self._stop_hold_reset_gap = 0.25
        self._stop_states = {
            "SELECT": {"start": None, "last": None},
            "SELECT2": {"start": None, "last": None},
        }
        self._shutdown_triggered = False

        # autorun settings
        self._autorun_active = False
        self._autorun_idle_threshold = 30
        self._autorun_duration = 10
        self._autorun_timer = None
        self._autorun_stop_event = threading.Event()
        self._autorun_queue = []
        self._autorun_index = 0
        self._autorun_any_input = False
        self._autorun_should_launch_next = False
        self._autorun_running_demo = False
        self._autorun_next_launch_at = 0
        self._autorun_cycle_gap = 1.0
        self._autorun_timeout_triggered = False
        
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
                if self._autorun_active:
                    self._start_autorun_timeout()
                self.queued(self.canvas, self.controller)
            except Exception as e:
                raise RuntimeError("Error occured running the selected program, within the selected program. ") from e
            finally:
                self._cancel_autorun_timeout()
                self.queued = None
                if self._autorun_active:
                    was_running = self._autorun_running_demo
                    self._autorun_running_demo = False
                    if was_running and not self._autorun_timeout_triggered:
                        self._autorun_any_input = True
                    if self._autorun_any_input:
                        self._autorun_active = False
                        self._autorun_should_launch_next = False
                        self._autorun_next_launch_at = 0
                        self._autorun_timeout_triggered = False
                    else:
                        self._autorun_should_launch_next = True
                        self._autorun_next_launch_at = time.time() + self._autorun_cycle_gap
                        self._autorun_timeout_triggered = False
                    self.autoRunTime = time.time()

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

        now = time.time()
        if self._autorun_active:
            if self._autorun_should_launch_next and now >= self._autorun_next_launch_at:
                self._queue_next_autorun_demo()
        elif self.isBasePath() and (now - self.autoRunTime) > self._autorun_idle_threshold:
            self.autoRunner()

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
        self._autorun_register_input()
        self.trackFPS = not self.trackFPS

    def selection_up(self):
        self._autorun_register_input()
        self.selection = (self.selection - 1) % len(self.options)
        self.autoRunTime = time.time()

    def selection_down(self):
        self._autorun_register_input()
        self.selection = (self.selection + 1) % len(self.options)
        self.autoRunTime = time.time()

    def enter(self):
        self._autorun_register_input()
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
            program = self._discover_program(getcwd())
            if program:
                self.queued = program
                self.running = False

        except Exception as e:
            print(
                "Something went wrong trying to look for or execute that program. Error:\n",
                e,
            )
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
                        and handle.name not in self.hidden_dirs
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
        self._autorun_register_input()
        self._handle_stop_hold("SELECT")

    def _select2_stop(self):
        self._autorun_register_input()
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

    def autoRunner(self):
        demos = self._collect_demos()
        if not demos:
            return

        self._autorun_queue = demos
        self._autorun_index = 0
        self._autorun_any_input = False
        self._autorun_should_launch_next = False
        self._autorun_active = True
        self._autorun_running_demo = False
        self._autorun_timeout_triggered = False
        self._queue_next_autorun_demo()

    def _discover_program(self, directory):
        module_name = path.basename(directory)
        if not module_name:
            return None

        module_name = module_name[0].upper() + module_name[1:]
        program_path = path.join(directory, f"{module_name}.py")

        if not path.isfile(program_path):
            return None

        module_spec = spec_from_file_location(module_name, program_path)
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        return getattr(module, module_name, None)

    def _start_autorun_timeout(self):
        self._autorun_stop_event.clear()
        self._autorun_timeout_triggered = False

        def wait_then_stop():
            if not self._autorun_stop_event.wait(self._autorun_duration):
                self._autorun_timeout_triggered = True
                self._invoke_select()

        self._autorun_timer = threading.Thread(target=wait_then_stop, daemon=True)
        self._autorun_timer.start()

    def _cancel_autorun_timeout(self):
        self._autorun_stop_event.set()
        self._autorun_timer = None

    def _invoke_select(self):
        try:
            if hasattr(self.controller, "function_map"):
                entry = self.controller.function_map.get("SELECT")
                if entry and "function" in entry:
                    entry["function"]()
                    return

            if hasattr(self.controller, "button_map") and hasattr(self.controller, "execution_map"):
                key = self.controller.button_map.get("SELECT")
                if key:
                    func = self.controller.execution_map.get(key)
                    if func:
                        func()
        except Exception as e:
            print(f"Failed to signal autorun stop: {e}")

    def _collect_demos(self):
        demos_path = path.join(self.base_path, "demos")
        demo_entries = []

        try:
            with scandir(demos_path) as directory:
                for handle in directory:
                    if handle.is_dir() and not handle.name.startswith("."):
                        program = self._discover_program(handle.path)
                        if program:
                            demo_entries.append((handle.path, program))
        except FileNotFoundError:
            return []

        demo_entries.sort(key=lambda item: item[0])
        return demo_entries

    def _queue_next_autorun_demo(self):
        if not self._autorun_queue:
            self._autorun_active = False
            self._autorun_should_launch_next = False
            return

        if self._autorun_index >= len(self._autorun_queue):
            self._autorun_index = 0

        selected_path, program = self._autorun_queue[self._autorun_index]
        self._autorun_index += 1

        try:
            chdir(selected_path)
            self._autorun_running_demo = True
            self._autorun_should_launch_next = False
            self._autorun_next_launch_at = 0
            self.autoRunTime = time.time()
            self.queued = program
            self.running = False
            self._autorun_stop_event.clear()
        except Exception as e:
            print(f"Failed to start autorun demo from {selected_path}: {e}")
            self._autorun_running_demo = False
            if self._autorun_index >= len(self._autorun_queue):
                self._autorun_active = False
                self._autorun_should_launch_next = False
            chdir(self.base_path)

    def _autorun_register_input(self):
        if not self._autorun_active:
            return

        self._autorun_any_input = True
        self._autorun_active = False
        self._autorun_should_launch_next = False
        self._autorun_running_demo = False
        self._autorun_queue = []
        self._cancel_autorun_timeout()
        self.autoRunTime = time.time()
        self._autorun_next_launch_at = 0
        self._autorun_timeout_triggered = False

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
