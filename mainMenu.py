from matrix_library import LEDWall, Canvas, Controller, shapes
from os import scandir, chdir, getcwd, path
from importlib.util import spec_from_file_location, module_from_spec
import time

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)


class MainMenu(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        # pointer to subclass to be executed on loop halt
        self.queued = None

        # options to select / current selection
        self.selection = 0
        self.options = []

        # set the path to start the menu at and get the options within
        self.base_path = path.dirname(path.abspath(__file__))
        chdir(self.base_path)
        self.getOptions()

        # begin the code
        super().__init__(canvas, controller, fps=15, trackFPS=True)

    def postLoop(self):
        if self.queued != None:
            try:
                self.queued(self.canvas, self.controller)
            except Exception as e:
                raise RuntimeError("Error occured running the selected program, within the selected program. ") from e
        
        if not self.__exited__:
            self.__init__(self.canvas, self.controller)

    def __draw__(self):
        titleColor = (50, 255, 50)

        title = shapes.Phrase("MENU", (self.canvas.width / 2, 5), titleColor, size=1.5)
        title.translate(0 - title.get_width() / 2, 0)
        self.canvas.add(title)

        for index, item in enumerate(self.options):
            itemColor = WHITE if self.selection != index else BLUE
            option = shapes.Phrase(
                item,
                (self.canvas.width / 2, self.canvas.height / 4 + index * 12),
                itemColor,
            )
            option.translate(0 - option.get_width() / 2, 0)
            self.canvas.add(option)

    def __bind_controls__(self):
        self.controller.add_function("UP", self.selection_up)
        self.controller.add_function("DOWN", self.selection_down)
        self.controller.add_function("A", self.enter)
        self.controller.add_function("Y", self.enter)
        self.controller.add_function("START", self.enter)
        self.controller.add_function("SELECT", self.__stop__)
        self.controller.add_function("UP2", self.selection_up)
        self.controller.add_function("DOWN2", self.selection_down)
        self.controller.add_function("A2", self.enter)
        self.controller.add_function("Y2", self.enter)
        self.controller.add_function("START2", self.enter)
        self.controller.add_function("SELECT2", self.__stop__)

    def selection_up(self):
        self.selection = (self.selection - 1) % len(self.options)

    def selection_down(self):
        self.selection = (self.selection + 1) % len(self.options)

    def enter(self):
        if self.options[self.selection] == "Exit":
            self.__stop__()

        elif self.options[self.selection] == "Back":
            chdir("..")
            self.options = []
            self.getOptions()

        else:
            chdir(self.options[self.selection])
            self.checkExecutable()
            self.options = []
            self.getOptions()

    def checkExecutable(self):
        try:
            with scandir() as directory:
                for handle in directory:
                    moduleName = f"{path.basename(getcwd())}"
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
        self.options.append("Exit")

    def isBasePath(self):
        return path.abspath(getcwd()) == path.abspath(self.base_path)


if __name__ == "__main__":
    canvas = Canvas(limitFps=False)
    # picture = shapes.Image(128,128)
    # picture.loadfile('startup.png')
    # canvas.add(picture)
    # canvas.draw()
    controller = Controller()
    #time.sleep(5)
    MainMenu(canvas, controller)
