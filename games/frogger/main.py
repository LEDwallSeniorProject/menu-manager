# Author: Josh Rainiel Julian <juj2@calvin.edu>
# Minor modifications by: Chris Wieringa <cwieri39@calvin.edu>
# Date: 2024-12-19

from matrix_library import shapes as s, canvas as c, controller as cont
import time, sys
from random import randrange


# Initializing the canvas
canvas = c.Canvas()
controller = cont.Controller()

# Defining the variables needed
frog_x = 65
frog_y = 121
frog_center = [frog_x, frog_y]

car1_x, car1_y = randrange(0,130), 107
car1_center = [car1_x,car1_y]

car2_x,car2_y = randrange(0,130), 93
car2_center = [car2_x,car2_y]

car3_x, car3_y = randrange(0,130), 79
car3_center = [car3_x, car3_y]

log1_start_x, log1_end_x, log1_y = 106, 135, 51
log1_start = [log1_start_x, log1_y]
log1_end = [log1_end_x, log1_y]

log2_start_x, log2_end_x, log2_y = 9, 38, 37
log2_start = [log2_start_x, log2_y]
log2_end = [log2_end_x, log2_y]

log3_start_x, log3_end_x, log3_y = 60, 89, 23
log3_start = [log3_start_x, log3_y]
log3_end = [log3_end_x, log3_y]

player_speed = 14
car_speed = 2
log_speed = 1.5

cooldown_time = 0.2

reseting = False

# Keep track of time of last action
last_action_time = time.time()

drawings_list = []

#### Controller functions
def controller_up():
    global frog_x, frog_y, player_speed, frog_center, last_action_time
    # Check if enough time has elapsed
    current_time = time.time()
    # Updates x and y values of the frog 
    frog_x = frog_center[0]
    frog_y = frog_center[1]
    if current_time - last_action_time > cooldown_time:
        if frog_is_inbounds(frog_x, frog_y,"up"):
            frog_y -= player_speed
            frog_center = [frog_x, frog_y]
        
        # Update my last action time
        last_action_time = current_time
def controller_down():
    global frog_x, frog_y, player_speed, frog_center, last_action_time
    
    # check if enough time has elapsed
    current_time = time.time()
    # Updates x and y values of the frog 
    frog_x = frog_center[0]
    frog_y = frog_center[1]
    if current_time - last_action_time > cooldown_time:
        if frog_is_inbounds(frog_x, frog_y,"down"):
            frog_y += player_speed
            frog_center = [frog_x, frog_y]
        
        # update my last action time
        last_action_time = current_time
        
def controller_left():
    global frog_x, frog_y, player_speed, frog_center, last_action_time
    
    # check if enough time has elapsed
    current_time = time.time()
    # Updates x and y values of the frog 
    frog_x = frog_center[0]
    frog_y = frog_center[1]
    if current_time - last_action_time > cooldown_time:
        if frog_is_inbounds(frog_x, frog_y,"left"):
            frog_x -= player_speed
            frog_center = [frog_x, frog_y]
        
        # update my last action time
        last_action_time = current_time
        
def controller_right():
    global frog_x, frog_y, player_speed, frog_center, last_action_time
    
    # check if enough time has elapsed
    # Updates x and y values of the frog 
    current_time = time.time()
    frog_x = frog_center[0]
    frog_y = frog_center[1]
    if current_time - last_action_time > cooldown_time:
        if frog_is_inbounds(frog_x, frog_y,"right"):
            frog_x += player_speed
            frog_center = [frog_x, frog_y]
        
        # update my last action time
        last_action_time = current_time

def gameover():
    global running
    running = False

        
#### Bind controller functions
controller.add_function('UP',controller_up)
controller.add_function('DOWN',controller_down)
controller.add_function('LEFT', controller_left)
controller.add_function('RIGHT', controller_right)
controller.add_function('START', gameover)


def move_obstacle(entity, direction, pixels):
    
    """ Takes in an entity and moves it 

    Parameters
    ---
    None
    
    Returns
    ---
    None
    
    Side Effects
    ---
    
    """
    global car1_x, car1_y, car1_center, car2_x, car2_y, car2_center, car3_x, car3_y, \
           car3_center, log1_start_x, log1_end_x, log1_start, log1_end, log2_start_x, log2_end_x, \
           log2_start, log2_end, log3_start_x, log3_end_x, log3_start, log3_end
    # Checks which direction the obstacle is trying to move
    if direction == 'left':
        # Checks which entity to move and moves the entity accordingly
        if entity == 'car1':
            car1_x -= pixels
            car1_center = [car1_x, car1_y]
        elif entity == 'car3':
            car3_x -= pixels
            car3_center = [car3_x, car3_y]
        elif entity == 'log1':   
            log1_start_x -= pixels
            log1_end_x -= pixels
            log1_start = [log1_start_x, log1_y]
            log1_end = [log1_end_x, log1_y]
        else:
            log3_start_x -= pixels
            log3_end_x -= pixels
            log3_start = [log3_start_x, log3_y]
            log3_end = [log3_end_x, log3_y]
    if direction == 'right':
        if entity == 'car2':    
            car2_x += pixels
            car2_center = [car2_x, car2_y]
        if entity == 'log2':
            log2_start_x += pixels
            log2_end_x += pixels
            log2_start = [log2_start_x, log2_y]
            log2_end = [log2_end_x, log2_y]
    
def obstacle_inbounds():
    """ Checks whether or not the moving obstacles are still within the bounds of the display screen, if they move of the screen,
        move them back to their original side so that they can be moved again across the display

    Parameters
    ---
    None
    
    Returns
    ---
    None
    """
    global car1_x, car1_y, car1_center, car2_x, car2_y, car2_center, car3_x, car3_y, \
           car3_center, log1_start_x, log1_end_x, log1_start, log1_end, log2_start_x, log2_end_x, \
           log2_start, log2_end, log3_start_x, log3_end_x, log3_start, log3_end
    if car1_x <= 0:
        car1_x = 130
        car1_center = [car1_x, car1_y]
        
    if car2_x >= 130:
        car2_x = 0
        car2_center = [car2_x, car2_y]
        
    if car3_x <= 0:
        car3_x = 130
        car3_center = [car3_x, car3_y]
    
    if log1_end_x <= -10:
        log1_start_x, log1_end_x = 130, 159
        log1_start = [log1_start_x, log1_y]
        log1_end = [log1_end_x, log1_y]
    
    if log2_start_x >= 140:
        log2_start_x, log2_end_x = -29,0
        log2_start = [log2_start_x, log2_y]
        log2_end = [log2_end_x, log2_y]
        
    if log3_end_x <= -10:
        log3_start_x, log3_end_x = 110, 139
        log3_start = [log3_start_x, log3_y]
        log3_end = [log3_end_x, log3_y]    
    

def car_collisions(frog, car):
    """ Checks whether or not two items are in contact with one another
    
    Parameters
    ---
    frog (int), x value of the frog entity
    
    car (int), x value of the car entity
    
    
    Returns
    ---
    None
    """
    global points 
    # If the cars are colliding
    if frog >= car - 7 and frog <= car + 7:
        # Reset Frog position
        lose_life()

def log_collisions(log_start, log_end, frog, direction):
    """ Checks the whether or not the log objects are colliding with the frog

    Parameters
    ---
    log_start (int), the starting x coordinate of the log
    
    log_end (int), the ending x coordinate of the log
    
    direction (str), a string that determines which direction the object is heading
    """
    
    global frog_x, frog_y, frog_center
   
   # Updates the frog x and y coordinates
   
    frog_x = frog_center[0]
    frog_y = frog_center[1]
    
    # Checks if the x coordinates of the frog are within the range of the log
    if frog >= log_start - 7 and frog <= log_end + 7 :
        # Moves the frog with the log depending on the direction the log is moving
        if direction == 'left':
            frog_x -= log_speed
            frog_center = [frog_x, frog_y]
        else:
            frog_x += log_speed
            frog_center = [frog_x, frog_y]
    else:
        # Sends the frog back to the origin if the frog is not on a log
        lose_life()

def lose_life():
    """ Moves frog back to original position and takes away one life, also displays a "you got hit" text

    Parameters
    ---
    None
    
    Returns
    ---
    None
    
    """
    global frog1_x, frog1_y, frog_center, lives
    
    # Sets the frog position back to original starting point
    frog1_x, frog1_y = 65, 121
    frog_center = [frog1_x,frog1_y]
    


    

def frog_is_inbounds(x, y, direction):
    """ Checks whether or not the entity is in bounds

    Parameters
    ---
    x (int) : X coordinate of the frog
    y (int) : Y coordinate of the frog
    direction (string) : Determines which direction the entity is attempting to move
    
    Returns
    ---
    None
    """
    if direction == "up":
        if y == 9:
            return False
        else:
            return True
    if direction == "down":
        if y == 121:
            return False
        else:
            return True
    if direction == "left":
        if x == 9:
            return False
        else:
            return True
        pass
    if direction == "right":
        if x == 121:
            return False
        else:
            return True
        
    
def crossed():
    """ Adds points to the user's score and sends the frog back to the start of the road

    Parameters
    ---
    None
    
    Returns
    ---
    None
    """
    global frog1_x, frog1_y, frog_center, lives
    
    # Sets frog's position back to original starting point
    frog1_x, frog1_y = 65, 121
    frog_center = [frog1_x,frog1_y]

def define_drawings():
    
    """ Defines all of the needed graphics that are to be displayed

    Parameters
    ---
    None
    
    Returns
    ---
    None
      
    
    """
    global drawings_list
    drawings_list = []
    
    road = s.Line((0,65), (127,65), (46,46,46), 100)
    drawings_list.append(road)

    water_center = (64, -5)
    water = s.Polygon(s.get_polygon_vertices(4,100,water_center),(51,209,255))
    water.rotate(45, water_center)
    drawings_list.append(water)

    grass1_center = (64,185)
    grass1 = s.Polygon(s.get_polygon_vertices(4,100,grass1_center),(124, 252, 0))
    grass1.rotate(45, grass1_center)
    drawings_list.append(grass1)

    grass2_center = (64, -57)
    grass2 = s.Polygon(s.get_polygon_vertices(4,100,grass2_center),(124,252,0))
    grass2.rotate(45, grass2_center)
    drawings_list.append(grass2)

    grass3 = s.Line((0, 65), (127, 65), (124, 255, 0),6)
    drawings_list.append(grass3)

    car1 = s.Polygon(s.get_polygon_vertices(4,5,car1_center),(255,0,0))
    car1.rotate(45,car1_center)
    drawings_list.append(car1)
    
    car2 = s.Polygon(s.get_polygon_vertices(4,5,car2_center),(255,0,0))
    car2.rotate(45,car2_center)
    drawings_list.append(car2)
    
    car3 = s.Polygon(s.get_polygon_vertices(4,5,car3_center),(255,0,0))
    car3.rotate(45,car3_center)
    drawings_list.append(car3)
    
    log1 = s.Line(log1_start,log1_end,(110, 38, 14),5.5)
    drawings_list.append(log1)
    
    log2 = s.Line(log2_start,log2_end,(110, 38, 14),5.5)
    drawings_list.append(log2)
    
    log3 = s.Line(log3_start,log3_end,(110, 38, 14),5.5)
    drawings_list.append(log3)
    
    
    frog = s.Polygon(s.get_polygon_vertices(10, 5, frog_center), (3, 116, 0))
    drawings_list.append(frog)



def draw_items():
    
    """ Adds all of the defined drawings to the canvas to be drawn
    
    Parameters
    ---
    None
    
    Returns
    ---
    None


    """
    # Clears the canvas from the old graphics
    canvas.clear()
    # Goes through list of drawings that need to be drawn and adds them to the canvas
    for graphics in drawings_list:
        canvas.add(graphics)
    canvas.draw()

# variable to say whether the game is running
running = True

# Main function: 
def main():
    while running:
        
        # Move all of the obstacles in their dedicated direction
        move_obstacle("car1", 'left', car_speed)
        move_obstacle("car2", 'right', car_speed)
        move_obstacle("car3", 'left', car_speed)
        move_obstacle("log1", 'left', log_speed)
        move_obstacle("log2", 'right', log_speed)
        move_obstacle("log3", 'left', log_speed)
        
        # Checks what y coordinate the frog is at and checks if it is colliding with its corresponding obstacle

        if frog_y == 107:
        
            car_collisions(frog_x,car1_x)
        
        elif frog_y == 93:
            
            car_collisions(frog_x,car2_x)
        
        elif frog_y == 79:
            
            car_collisions(frog_x,car3_x)
        
        elif frog_y == 51:
            
            log_collisions(log1_start_x, log1_end_x, frog_x,'left')
        
        elif frog_y == 37:
            
            log_collisions(log2_start_x, log2_end_x, frog_x,'right')
        
        elif frog_y == 23:
            
            log_collisions(log3_start_x, log3_end_x, frog_x,'left')
        
        elif frog_y == 9:
            
            crossed()
        obstacle_inbounds()
        define_drawings()
        draw_items()
        time.sleep(1/60)

main()

# Print GAME OVER!
canvas.clear()
canvas.add(s.Phrase("GAME OVER", [32, 64], size=1))
canvas.draw()
time.sleep(2)

# Clean quit here
print("quit")
sys.exit(0)