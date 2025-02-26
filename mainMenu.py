from matrix_library import LEDWall, Canvas, Controller, shapes
import os 

WHITE = (255,255,255)
BLUE = (50,100,255)

class MainMenu(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.queued = None
        self.selection = 0
        self.options = []
        self.getOptions()

        
        #begin the code
        super().__init__(canvas, controller)

    def __loop__(self):
        super().__loop__()
        if self.queued != None:
            self.queued(self.canvas, self.controller)

    def __draw__(self):
        titleColor = (50, 255, 50)

        title = shapes.Phrase("MENU", (self.canvas.width/2, 5), titleColor, size=1.5)
        title.translate(0-title.get_width()/2, 0)
        self.canvas.add(title)

        for index, item in enumerate(self.options):
            itemColor = WHITE if self.selection != index else BLUE
            option = shapes.Phrase(item, (self.canvas.width/2, self.canvas.height/4 +index*12), itemColor)
            option.translate(0-option.get_width()/2, 0)
            self.canvas.add(option)

    def __bind_controls__(self):
        self.controller.add_function("UP", self.selection_up)
        self.controller.add_function("DOWN", self.selection_down)
        self.controller.add_function("A", self.enter)
        self.controller.add_function("Y", self.enter)
        self.controller.add_function("START", self.enter)
        self.controller.add_function("SELECT", self.exit)

    def selection_up(self):
        self.selection = (self.selection-1)%len(self.options)

    def selection_down(self):
        self.selection = (self.selection+1)%len(self.options)

    def enter(self):
        self.running = False

        

        if self.options[self.selection] == 'Exit':
            self.exit()
        
        else:
            raise RuntimeError("Code Error; No Item Selected")

    def getOptions(self):
        try:
            with os.scandir() as directory:
                for handle in directory:
                    if not handle.name.startswith('.') and not handle.name.startswith('__') and handle.is_dir():
                        self.options.append(handle.name)
                        
        except Exception as e:
            raise Exception("Something went wrong trying to look for options in the current directory") from e
        
        self.options.sort()
        self.options.append('Exit')

if __name__ == "__main__":
    MainMenu(Canvas(), Controller())
    
