from matrix_library import LEDWall, Canvas, Controller, shapes
from random import randrange
import time


class Frogger(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        # Define any of your variables here
        # Defining the variables needed
        self.frog_x = 65
        self.frog_y = 121
        self.frog_center = [self.frog_x, self.frog_y]

        self.car1_x, self.car1_y = randrange(0, 130), 107
        self.car1_center = [self.car1_x, self.car1_y]

        self.car2_x, self.car2_y = randrange(0, 130), 93
        self.car2_center = [self.car2_x, self.car2_y]  # Fixed missing self.

        self.car3_x, self.car3_y = randrange(0, 130), 79
        self.car3_center = [self.car3_x, self.car3_y]  # Fixed missing self.

        self.log1_start_x, self.log1_end_x, self.log1_y = 106, 135, 51
        self.log1_start = [self.log1_start_x, self.log1_y]
        self.log1_end = [self.log1_end_x, self.log1_y]  # Added self.

        self.log2_start_x, self.log2_end_x, self.log2_y = 9, 38, 37
        self.log2_start = [self.log2_start_x, self.log2_y]
        self.log2_end = [self.log2_end_x, self.log2_y]  # Added self.

        self.log3_start_x, self.log3_end_x, self.log3_y = 60, 89, 23
        self.log3_start = [self.log3_start_x, self.log3_y]
        self.log3_end = [self.log3_end_x, self.log3_y]  # Added self.

        self.player_speed = 14
        self.car_speed = 2
        self.log_speed = 1.5

        self.cooldown_time = 0.1

        self.reseting = False
        self.lives = 3
        self.score = 0

        # Keep track of time of last action
        self.last_action_time = time.time()
                
        # begin the code (this triggers execution of the loop)
        super().__init__(canvas, controller, trackFPS=False)

    # REQUIRED FUNCTION
    # this function will run every frame
    # and should contain graphics code
    # AND logic updates
    def __draw__(self):
        # Move all of the obstacles in their dedicated direction
        self.move_obstacle("car1", "left", self.car_speed)
        self.move_obstacle("car2", "right", self.car_speed)
        self.move_obstacle("car3", "left", self.car_speed)
        self.move_obstacle("log1", "left", self.log_speed)
        self.move_obstacle("log2", "right", self.log_speed)
        self.move_obstacle("log3", "left", self.log_speed)

        # Checks what y coordinate the frog is at and checks if it is colliding with its corresponding obstacle
        if self.frog_y == 107:
            self.car_collisions(self.frog_x, self.car1_x)

        elif self.frog_y == 93:
            self.car_collisions(self.frog_x, self.car2_x)

        elif self.frog_y == 79:
            self.car_collisions(self.frog_x, self.car3_x)

        elif self.frog_y == 51:
            self.log_collisions(self.log1_start_x, self.log1_end_x, self.frog_x, "left")

        elif self.frog_y == 37:
            self.log_collisions(
                self.log2_start_x, self.log2_end_x, self.frog_x, "right"
            )

        elif self.frog_y == 23:
            self.log_collisions(self.log3_start_x, self.log3_end_x, self.frog_x, "left")

        elif self.frog_y == 9:
            self.crossed()

        self.obstacle_inbounds()
        self.define_drawings()

    def toggle_track_fps(self):
        self.trackFPS = not self.trackFPS

    # REQUIRED FUNCTION
    # this function will run once at super().__init__()
    # and should contain mappings to control the program
    def __bind_controls__(self):
        self.controller.add_function("LB", self.toggle_track_fps)
        self.controller.add_function("UP", self.controller_up)
        self.controller.add_function("DOWN", self.controller_down)
        self.controller.add_function("LEFT", self.controller_left)
        self.controller.add_function("RIGHT", self.controller_right)
        self.controller.add_function("SELECT", self.quit)

    #### Controller functions
    def controller_up(self):
        # Check if enough time has elapsed
        current_time = time.time()
        # Updates x and y values of the frog
        self.frog_x = self.frog_center[0]
        self.frog_y = self.frog_center[1]
        if current_time - self.last_action_time > self.cooldown_time:
            if self.frog_is_inbounds(self.frog_x, self.frog_y, "up"):
                self.frog_y -= self.player_speed
                self.frog_center = [self.frog_x, self.frog_y]

            # Update last action time
            self.last_action_time = current_time

    def controller_down(self):
        # Check if enough time has elapsed
        current_time = time.time()
        # Updates x and y values of the frog
        self.frog_x = self.frog_center[0]
        self.frog_y = self.frog_center[1]
        if current_time - self.last_action_time > self.cooldown_time:
            if self.frog_is_inbounds(self.frog_x, self.frog_y, "down"):
                self.frog_y += self.player_speed
                self.frog_center = [self.frog_x, self.frog_y]

            # Update last action time
            self.last_action_time = current_time

    def controller_left(self):
        # Check if enough time has elapsed
        current_time = time.time()
        # Updates x and y values of the frog
        self.frog_x = self.frog_center[0]
        self.frog_y = self.frog_center[1]
        if current_time - self.last_action_time > self.cooldown_time:
            if self.frog_is_inbounds(self.frog_x, self.frog_y, "left"):
                self.frog_x -= self.player_speed
                self.frog_center = [self.frog_x, self.frog_y]

            # Update last action time
            self.last_action_time = current_time

    def controller_right(self):
        # Check if enough time has elapsed
        current_time = time.time()
        # Updates x and y values of the frog
        self.frog_x = self.frog_center[0]
        self.frog_y = self.frog_center[1]
        if current_time - self.last_action_time > self.cooldown_time:
            if self.frog_is_inbounds(self.frog_x, self.frog_y, "right"):
                self.frog_x += self.player_speed
                self.frog_center = [self.frog_x, self.frog_y]

            # Update last action time
            self.last_action_time = current_time

    def game_over(self):
        if self.running == True:
            raise ValueError("self.running == True but game has ended")
        self.canvas.clear()
        self.canvas.add(shapes.Phrase("GAME OVER", [32, 64], size=1))
        self.canvas.draw()
        time.sleep(5)

    def move_obstacle(self, entity, direction, pixels):
        """Takes in an entity and moves it."""

        # Checks which direction the obstacle is trying to move
        if direction == "left":
            # Checks which entity to move and moves the entity accordingly
            if entity == "car1":
                self.car1_x -= pixels
                self.car1_center = [self.car1_x, self.car1_y]
            elif entity == "car3":
                self.car3_x -= pixels
                self.car3_center = [self.car3_x, self.car3_y]
            elif entity == "log1":
                self.log1_start_x -= pixels
                self.log1_end_x -= pixels
                self.log1_start = [self.log1_start_x, self.log1_y]
                self.log1_end = [self.log1_end_x, self.log1_y]
            else:
                self.log3_start_x -= pixels
                self.log3_end_x -= pixels
                self.log3_start = [self.log3_start_x, self.log3_y]
                self.log3_end = [self.log3_end_x, self.log3_y]
        if direction == "right":
            if entity == "car2":
                self.car2_x += pixels
                self.car2_center = [self.car2_x, self.car2_y]
            if entity == "log2":
                self.log2_start_x += pixels
                self.log2_end_x += pixels
                self.log2_start = [self.log2_start_x, self.log2_y]
                self.log2_end = [self.log2_end_x, self.log2_y]

    def obstacle_inbounds(self):
        """Checks whether or not the moving obstacles are still within the bounds of the display screen."""

        if self.car1_x <= 0:
            self.car1_x = 130
            self.car1_center = [self.car1_x, self.car1_y]

        if self.car2_x >= 130:
            self.car2_x = 0
            self.car2_center = [self.car2_x, self.car2_y]

        if self.car3_x <= 0:
            self.car3_x = 130
            self.car3_center = [self.car3_x, self.car3_y]

        if self.log1_end_x <= -10:
            self.log1_start_x, self.log1_end_x = 130, 159
            self.log1_start = [self.log1_start_x, self.log1_y]
            self.log1_end = [self.log1_end_x, self.log1_y]

        if self.log2_start_x >= 140:
            self.log2_start_x, self.log2_end_x = -29, 0
            self.log2_start = [self.log2_start_x, self.log2_y]
            self.log2_end = [self.log2_end_x, self.log2_y]

        if self.log3_end_x <= -10:
            self.log3_start_x, self.log3_end_x = 110, 139
            self.log3_start = [self.log3_start_x, self.log3_y]
            self.log3_end = [self.log3_end_x, self.log3_y]

    def car_collisions(self, frog, car):
        """Checks whether or not two items are in contact with one another."""

        # If the cars are colliding
        if frog >= car - 7 and frog <= car + 7:
            # Reset Frog position
            self.lose_life()

    def log_collisions(self, log_start, log_end, frog, direction):
        """Checks whether or not the log objects are colliding with the frog."""

        # Updates the frog x and y coordinates
        self.frog_x = self.frog_center[0]
        self.frog_y = self.frog_center[1]

        # Checks if the x coordinates of the frog are within the range of the log
        if frog >= log_start - 7 and frog <= log_end + 7:
            # Moves the frog with the log depending on the direction the log is moving
            if direction == "left":
                self.frog_x -= self.log_speed
                self.frog_center = [self.frog_x, self.frog_y]
            else:
                self.frog_x += self.log_speed
                self.frog_center = [self.frog_x, self.frog_y]
        else:
            # Sends the frog back to the origin if the frog is not on a log
            self.lose_life()

    def lose_life(self):
        """Moves frog back to original position and takes away one life."""

        # Sets the frog position back to the original starting point
        self.frog1_x, self.frog1_y = 65, 121
        self.frog_center = [self.frog1_x, self.frog1_y]

        # Reduce lives (assuming lives is an instance attribute)
        self.lives -= 1
        if self.lives <= 0:
            self.quit()

    def frog_is_inbounds(self, x, y, direction):
        """Checks whether or not the entity is in bounds."""

        if direction == "up":
            return y != 9
        if direction == "down":
            return y != 121
        if direction == "left":
            return x != 9
        if direction == "right":
            return x != 121
        return False  # Default case if an invalid direction is given

    def crossed(self):
        """Adds points to the user's score and sends the frog back to the start of the road."""

        # Sets frog's position back to the original starting point
        self.frog1_x, self.frog1_y = 65, 121
        self.frog_center = [self.frog1_x, self.frog1_y]

        # Assuming you are tracking score, you may want to increment it
        self.score += 1

    def define_drawings(self):
        """Defines all of the needed graphics that are to be displayed."""

        self.drawings_list = []

        road = shapes.Line((0, 65), (127, 65), (46, 46, 46), 100)
        self.drawings_list.append(road)

        water_center = (64, -5)
        water = shapes.Polygon(
            shapes.get_polygon_vertices(4, 100, water_center), (51, 209, 255)
        )
        water.rotate(45, water_center)
        self.drawings_list.append(water)

        grass1_center = (64, 185)
        grass1 = shapes.Polygon(
            shapes.get_polygon_vertices(4, 100, grass1_center), (124, 252, 0)
        )
        grass1.rotate(45, grass1_center)
        self.drawings_list.append(grass1)

        grass2_center = (64, -57)
        grass2 = shapes.Polygon(
            shapes.get_polygon_vertices(4, 100, grass2_center), (124, 252, 0)
        )
        grass2.rotate(45, grass2_center)
        self.drawings_list.append(grass2)

        grass3 = shapes.Line((0, 65), (127, 65), (124, 255, 0), 6)
        self.drawings_list.append(grass3)

        car1 = shapes.Polygon(
            shapes.get_polygon_vertices(4, 5, self.car1_center), (255, 0, 0)
        )
        car1.rotate(45, self.car1_center)
        self.drawings_list.append(car1)

        car2 = shapes.Polygon(
            shapes.get_polygon_vertices(4, 5, self.car2_center), (255, 0, 0)
        )
        car2.rotate(45, self.car2_center)
        self.drawings_list.append(car2)

        car3 = shapes.Polygon(
            shapes.get_polygon_vertices(4, 5, self.car3_center), (255, 0, 0)
        )
        car3.rotate(45, self.car3_center)
        self.drawings_list.append(car3)

        log1 = shapes.Line(self.log1_start, self.log1_end, (110, 38, 14), 5.5)
        self.drawings_list.append(log1)

        log2 = shapes.Line(self.log2_start, self.log2_end, (110, 38, 14), 5.5)
        self.drawings_list.append(log2)

        log3 = shapes.Line(self.log3_start, self.log3_end, (110, 38, 14), 5.5)
        self.drawings_list.append(log3)

        frog = shapes.Polygon(
            shapes.get_polygon_vertices(10, 5, self.frog_center), (3, 116, 0)
        )
        self.drawings_list.append(frog)

        for graphics in self.drawings_list:
            self.canvas.add(graphics)

    # OPTIONAL FUNCTION
    # this function will override the __loop__() function
    # use super().__loop__() if you just want to add code
    # before the loop begins or after it ends
    # or write your own looping
    def __loop__(self):
        super().__loop__()
        self.game_over()


# every program needs this line
if __name__ == "__main__":
    Frogger(Canvas(), Controller())
