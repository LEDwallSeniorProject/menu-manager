from LEDWall import *

WHITE = (255,255,255)
BLUE = (50,100,255)

class GamesMenu(LEDProgram):
    def __init__(self, canvas, controller):
        self.queued = None
        self.selection = 0
        self.options = ['a', 'b', 'c']

        #begin the code
        super().__init__(canvas, controller)


    def __loop__(self):
        super().__loop__()
        if self.queued != None:
            self.queued(self.canvas, self.controller)

    def __draw__(self):
        titleColor = (50, 255, 50)

        title = Shapes.Phrase("MENU", (self.canvas.width/2, 5), titleColor, size=1.5)
        title.translate(0-title.get_width()/2, 0)
        self.canvas.add(title)

        for index, item in enumerate(self.options):
            itemColor = WHITE if self.selection != index else BLUE
            option = Shapes.Phrase(item, (self.canvas.width/2, self.canvas.height/4 +index*12), itemColor)
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

        if self.options[self.selection] == 'a':
            import gamesMenu
            self.queued = gamesMenu.GamesMenu

        elif self.options[self.selection] == 'b':
            self.exit()

        else:
            raise RuntimeError("Code Error; No Item Selected")
        
        
if __name__ == "__main__":
    GamesMenu(matrix.Canvas(), matrix.Controller())
    
   
