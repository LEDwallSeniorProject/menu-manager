from matrix_library import LEDWall, Canvas, Controller, shapes
import matrix_library as matrix
import time


class Snake(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        # define any of your variables here
        self.snake_pos = [16, 16]
        self.snake_body = [[16, 16], [15, 16], [14, 16]]
        self.snake_dir = [1, 0]

        self.food_spawned = True
        self.food_pos = [16, 8]
        self.__fps__ = 10

        # begin the code (this triggers execution of the loop)
        super().__init__(canvas, controller)

    # REQUIRED FUNCTION
    # this function will run every frame
    # and should contain graphics code
    # and updates
    def __draw__(self):
        if self.snake_pos == self.food_pos:
            self.food_spawned = False
        for pos in self.snake_body:
            verts = matrix.get_polygon_vertices(4, 2, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
            body = matrix.Polygon(verts, (0, 255, 0))
            body.rotate(45, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
            self.canvas.add(body)

        self.snake_body.insert(0, self.snake_pos.copy())
        if self.snake_pos != self.food_pos:
            self.snake_body.pop()

        if not self.food_spawned:
            self.food_pos = [(int(time.time()) % 28) + 2, (int(time.time()) % 28) + 2]
            self.food_spawned = True

        food = matrix.Polygon(
            matrix.get_polygon_vertices(
                4, 2, ((self.food_pos[0] * 4) + 2, (self.food_pos[1] * 4) + 2)
            ),
            (255, 0, 0),
        )
        food.rotate(45, ((self.food_pos[0] * 4) + 2, (self.food_pos[1] * 4) + 2))

        self.canvas.add(food)

        self.snake_pos[0] += self.snake_dir[0]
        self.snake_pos[1] += self.snake_dir[1]

        if self.snake_pos[0] < 0 or self.snake_pos[0] >= 33 or self.snake_pos[1] < 0 or self.snake_pos[1] >= 33:
            self.running = False

        if self.snake_pos in self.snake_body:
            self.running = False


    def postLoop(self):
        self.canvas.clear()
        self.canvas.add(matrix.Phrase("GAME OVER", [32, 64], size=1))
        self.canvas.draw()
        time.sleep(1)


    # REQUIRED FUNCTION
    # this function will run once at super().__init__()
    # and should contain mappings to control the program
    def __bind_controls__(self):
        self.controller.add_function("UP", self.up)
        self.controller.add_function("DOWN", self.down)
        self.controller.add_function("LEFT", self.left)
        self.controller.add_function("RIGHT", self.right)


    # Setup the controller functions
    def up(self):
        self.snake_dir = [0, -1]

    def down(self):
        self.snake_dir = [0, 1]

    def left(self):
        self.snake_dir = [-1, 0]

    def right(self):
        self.snake_dir = [1, 0]


    # code defined here will run before the main loop begins 
    #   but after all init is done
    def preLoop(self):
        pass

    # this code runs after the loop has run
    def postLoop(self):
        pass

# every program needs this line
if __name__ == "__main__":
    Snake(Canvas(), Controller())
