import matrix_library as matrix 
from matrix_library import shapes as Shapes
import time

class LEDProgram:
    def __init__(self, canvas, controller):
        self.canvas = canvas
        self.controller = controller
        # check that things are defined correctly
        try:
            self.__bind_controls__
            self.__draw__
            self.__loop__
            self.__unbind_controls__
            self.exit

        except AttributeError as e:
            error = """
            Not all required functions are bound.
            Required functions:
                self.__bind_controls__
                self.__draw__
            """
            raise Exception(error) from e

        self.__bind_controls__()
        self.running = True
        self.__loop__()


    """
    Feel free to add code to this by creating your own function 
    called __loop__() in your child class and calling this with super()
    """
    def __loop__(self):

        last_time = time.time()
        fps = 60
        frame_time = 1/fps
        frames = 0

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - last_time
            
            if elapsed_time > frame_time:
                last_time = current_time
                frames += 1 

                self.canvas.clear()
                self.__draw__()
                self.canvas.draw()

        self.__unbind_controls__()


    def __unbind_controls__(self):
        self.controller.clear()

    def exit(self):
        self.running = False
        self.controller.stop()
        

if __name__ == "__main__":
    Program(matrix.Canvas(), matrix.Controller())
    
