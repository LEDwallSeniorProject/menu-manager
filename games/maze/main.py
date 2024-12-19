# Author: Ben Skillen <bcs29@calvin.edu>
# Minor modifications by: Chris Wieringa <cwieri39@calvin.edu>
# Date: 2024-12-17

from matrix_library import canvas as c, shapes as s, Controller as ctrl
from random import randint
import time, sys

class maze_app:
    """An app which produces a maze
        
    Attributes
    ----------
    self.canvas: the window the maze is presented in
    
    self.limits: a variable which limits the distance one of the lines can travel
    
    self.stiles: a list of each individual turning point along the maze's solution path
    
    self.matrix: a matrix containing each point in the 128x128 grid, and what color to print it
    
    self.coord: a store of which coordinate is being worked on

    self.running: a boolean that says whether the game is being played right now
    
    Functions
    ---------
    self.__init__: the initialization function, this uses the proper sequence to generate and
                   run the maze game
                   
    self.controls: Given a controller input, assigns the controller functions for the necessary
                   buttons
                   
    self.gen_maze: Creates a matrix with 1's to represent walkable paths and 0's to represent walls
    
    self.draw: Prints self.matrix onto self.canvas
    
    self.check_move: Checks if a given move would follow a path or run into a wall
    
    self.move_left	: Moves the character left
    self.move_right	: 					 right
    self.move_up	:   				    up
    self.move_down	: 					  down
    
    self.gen_dead_ends: Takes the maze with it's correct path and fills in the empty space with
                        false paths and dead ends
                    
    self.draw_end: Creates a draw_end border around the maze, and adds the destination square at the bottom right
    
    self.check_end: Checks if a given empty point, when extended in a given direction, hits the edge of the
                    screen before hitting part of the maze
                    
    self.dead_end: Draws a dead end from the given point to a point in the maze
    
    self.line_find: Given two coordinates, add a line between the two in the matrix
    """
    def __init__(self):
        """Initialize Class.

        Calls all necessary functions, then runs the
        print and movement cycle to run the game
        
        Parameters
        ----------
        none
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Presents a random maze, and repeatedly prints
        it out, allowing the player's location to change
        """
        self.canvas = c.Canvas((100,100,100))	#Initialize the canvas
        self.limits = [1,1]
        self.stiles = []
        
        self.matrix = []
        for i in range(63):
            self.matrix.append(63*[0])			#Create a 64x64 matrix with all 0's
        
        self.stileMatrix = []
        for i in range(32):
            self.stileMatrix.append(32*[0])		#Create a 32x32 matrix with all 0's for faster work with the turning points
            
        self.coord = (1,1)
        self.stiles.append(self.coord)			#Adds the first point to the list of Stiles
        
        self.stileMatrix[self.coord[0]][self.coord[1]] = 1 #Sets the matrix input at the given coordinate to 1
        
        self.gen_maze()
        self.gen_dead_ends()
        self.draw_end()
        self.draw()
        # ^ Create the maze in these four steps
        
        self.coord = [2,2]
        
        control = ctrl()
        control = self.controls(control)
        #initialize the controller
        
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1),(200,50,100)))
        #draws the initial position of the character

        # start the game
        self.running = True

        while self.running:
            self.canvas.draw()
            time.sleep(0.1)
            #update the canvas as the objects on it change

        # print game over!
        self.canvas.clear()
        self.canvas.add(s.Phrase("GAME OVER", [32, 64], size=1))
        self.canvas.draw()
        time.sleep(2)

            
    def quit(self):
        """ Quits the program
        
        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing
    
        Side effects
        ------------
        Clears the matrix
        """
        self.running = False

    def controls(self, controller):
        """Sets up Controller
        
        Parameters
        ----------
        Controller: The controller object that the functions
        are to be tied to
        
        Returns
        -------
        Controller: The controller object with new
        Up, Down, Left, and Right functions.
    
        Side effects
        ------------
        None
        """
        controller.add_function("UP",self.move_up)
        controller.add_function("LEFT",self.move_left)
        controller.add_function("DOWN",self.move_down)
        controller.add_function("RIGHT",self.move_right)
        controller.add_function("START",self.quit)
        return(controller)
    
          
    def gen_maze(self):
        """Randomly generates a maze matrix
        
        Parameters
        ----------
        None          
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Makes self.matrix into a maze, representing paths
        as 1s and walls as 0s
        """
        #This code generates the main path that leads to the end
        ordinal = randint(0,1)		#First, it chooses a random axis on which to move, 0 representing up and down, 1 representing right and left
        stileX = []					#Start a list of the points at which the path turns
        complexity = randint(25,31) #Choose the number of moves the maze will make along its main path
        for i in range(complexity): #repeat this process a number of times equal to the number of moves
            if ordinal == 1: 
                if self.coord[1] >= self.limits[1]: #Check to ensure the maze won't overlap itself
                    self.coord = [randint(1,32-complexity+i), self.coord[1]] #Move the path to a random point along the given axis
                    stileX.append(self.coord[0]) #add the new point to the temporary list of stiles
                else:
                    self.coord = [randint(self.limits[0],32-complexity+i), self.coord[1]]
                    stileX.append(self.coord[0])
                ordinal = 0
                if self.coord[0] >= self.limits[0]:
                    self.limits[0] = self.coord[0]
            else:
                if self.coord[0] >= self.limits[0]:
                    self.coord = [self.coord[0], randint(1,32-complexity+i)]
                    stileX.append(self.coord[0])
                else:
                    self.coord = [self.coord[0], randint(self.limits[1],32-complexity+i)]
                ordinal = 1
                if self.coord[1] >= self.limits[1]:
                    self.limits[1] = self.coord[1]
                #Further statements in the above section follow the same pattern, but with different values
            self.stiles.append(self.coord) #Add the temporary stiles to the permanent list
            self.stileMatrix[self.coord[0]][self.coord[1]] = 1
            self.line_find(self.coord, self.stiles[i])
        if ordinal == 1:	#finally make a line from the final stile to the edge of the maze, then to the bottom right.
            self.coord = [31, self.coord[1]]
            self.stiles.append(self.coord)
            self.line_find(self.coord, self.stiles[i+1])
            self.coord = [31, 31]
            self.line_find(self.coord, self.stiles[i+2])
        else:
            self.coord = [self.coord[0], 31]
            self.stiles.append(self.coord)
            self.line_find(self.coord, self.stiles[i+1])
            self.coord = [31,31]
            self.line_find(self.coord, self.stiles[i+2])
        self.stiles.append(self.coord)
        

    def draw(self):
        """Prints the self.matrix to the canvas
        
        Parameters
        ----------
        none
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Translates the self.matrix attribute into a
        printable screen for the 128x128 pixel grid
        """
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if self.matrix[row][col] == 1:	#because the maze has 4 pixels per unit, this draws cells with four add pixel statements
                    self.canvas.add(s.Pixel((2*col, 2*row), (0,0,0)))
                    self.canvas.add(s.Pixel((2*col-1, 2*row), (0,0,0)))
                    self.canvas.add(s.Pixel((2*col, 2*row-1), (0,0,0)))
                    self.canvas.add(s.Pixel((2*col-1, 2*row-1), (0,0,0)))
      
      
    def check_move(self,coord):
        """Given a coordinate, it checks if that coordinate is
        a valid path block, or a wall
        
        Parameters
        ----------
        coord: The coordinate to be checked     
        
        Returns
        -------
        True if the coordinate is part of the path, and False
        if the coordinate is a wall.
    
        Side effects
        ------------
        None
        """
        try: #Check if the given point is within the matrix
            if self.matrix[coord[1]][coord[0]] == 1:
                pass
        except:
            return(False)
        
        #Check if the given point is a wall or part of the path
        if self.matrix[coord[1]][coord[0]] == 1:
            return(True)
        else:
            return(False)
    
    
    def move_left(self):
        """Moves the character one space leftwards.
        
        Parameters
        ----------
        None          
        
        Returns
        -------
        None
    
        Side effects
        ------------
        if the coordinate directly to the left of the
        current one is not a wall, it replaces the current
        coordinate with a darker hue, and makes the leftward
        coordinate the brighter pink color.
        """
        #replace the current pixel with an old color
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (100,25,50)))
        temp_coord = [self.coord[0]-1,self.coord[1]]
        if self.check_move(temp_coord): #run self.check_move(temp_coord) to see if the move is valid, and move the pixel if it is
            self.coord = temp_coord
        #print the pixel in a brighter color, where it was originally if the move is invalid, and at its new point if the move is valid 
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (200,50,100)))
        
        
    def move_right(self):
        """Moves the character one space rightwards.
        
        Parameters
        ----------
        None          
        
        Returns
        -------
        None
    
        Side effects
        ------------
        if the coordinate directly to the right of the
        current one is not a wall, it replaces the current
        coordinate with a darker hue, and makes the rightward
        coordinate the brighter pink color.
        """
        #replace the current pixel with an old color
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (100,25,50)))
        temp_coord = [self.coord[0]+1,self.coord[1]]
        if self.check_move(temp_coord): #run self.check_move(temp_coord) to see if the move is valid, and move the pixel if it is
            self.coord = temp_coord
        #print the pixel in a brighter color, where it was originally if the move is invalid, and at its new point if the move is valid 
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (200,50,100)))
        
        
    def move_up(self):
        """Moves the character one space upwards.
        
        Parameters
        ----------
        None          
        
        Returns
        -------
        None
    
        Side effects
        ------------
        if the coordinate directly to the up from the
        current one is not a wall, it replaces the current
        coordinate with a darker hue, and makes the upward
        coordinate the brighter pink color.
        """
        #replace the current pixel with an old color
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (100,25,50)))
        temp_coord = [self.coord[0],self.coord[1]-1]
        if self.check_move(temp_coord): #run self.check_move(temp_coord) to see if the move is valid, and move the pixel if it is
            self.coord = temp_coord
        #print the pixel in a brighter color, where it was originally if the move is invalid, and at its new point if the move is valid 
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (200,50,100)))    
        
        
    def move_down(self):
        """Moves the character one space downwards.
        
        Parameters
        ----------
        None          
        
        Returns
        -------
        None
    
        Side effects
        ------------
        if the coordinate directly downwards from the
        current one is not a wall, it replaces the current
        coordinate with a darker hue, and makes the downward
        coordinate the brighter pink color.
        """
        #replace the current pixel with an old color
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (100,25,50)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (100,25,50)))
        temp_coord = [self.coord[0],self.coord[1]+1]
        if self.check_move(temp_coord): #run self.check_move(temp_coord) to see if the move is valid, and move the pixel if it is
            self.coord = temp_coord
        #print the pixel in a brighter color, where it was originally if the move is invalid, and at its new point if the move is valid 
        self.canvas.add(s.Pixel((2*self.coord[0],2*self.coord[1]),(200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0], 2*self.coord[1]-1), (200,50,100)))
        self.canvas.add(s.Pixel((2*self.coord[0]-1, 2*self.coord[1]-1), (200,50,100)))


    def gen_dead_ends(self):
        """Fills out the maze with dead ends
        
        Parameters
        ----------
        none
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Goes over every unconnected point in the maze to
        add a dead-end connecting to the main maze
        """
        #Create a list of all relevant points which aren't part of the maze yet
        empty = []
        for row in range(1,len(self.stileMatrix)-1):
            for col in range(1,len(self.stileMatrix[row])-1):
                if self.matrix[2*row][2*col] == 0:
                    empty.append([row,col])
                    
        #Randomly choose a point on this list, and using the self.dead_end() function
        #create a dead end from that point towards a part of the maze.
        while len(empty) > 0:
            temp = empty[randint(0,len(empty)-1)]
            compass = ((1,0),(0,1),(-1,0),(0,-1))[randint(0,3)]
            while self.check_end(temp,compass) == False:
                compass = ((1,0),(0,1),(-1,0),(0,-1))[randint(0,3)]
            self.dead_end(temp, compass)
            empty.remove(temp)
            
            
    def draw_end(self):
        """Adds an ending point to the maze
        
        Parameters
        ----------
        none
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Creates a border of non-accessible area
        around the maze.
        """
        #Make a 3x3 region in the bottom right of the maze which constitutes the ending
        for row in range(3):
            for col in range(3):
                self.matrix[62-col][62-row] = 1
            
            
    def check_end(self, point, direction):
        """Checks if 
        
        Parameters
        ----------
        point: a tuple that gives a point on the maze
               for the function to check
            
        direction: a tupple from the set ((1,0), (0,1), (-1,0), (0,-1)),
                   which dictates the direction for this function to check
        
        Returns
        -------
        True or False, depending on whether that direction includes another
        part of the maze. If going from that point in that direction
        reaches another part of the maze, it returns True, while if it
        reaches the edge of the maze it returns False.
    
        Side effects
        ------------
        None
        """
        #default the check value to True
        check = True
        point = [2*point[0], 2*point[1]] #translate between the stile matrix and the normal matrix
        while self.matrix[point[0]][point[1]] == 0:	#runs until it reaches a point in the maze, or the edge of the screen
            point = [point[0] + 2*direction[0], point[1] + 2*direction[1]]
            if not(1 < point[0] < 63 and 1 < point[1] < 63): #if the function reaches the edge, make "check" false, and break from the for statement
                check = False
                break
        return check
        
        
    def dead_end(self,point, direction):
        """Draws a line from the selected point in the
        selected direction until it reaches another part
        of the maze.
        
        Parameters
        ----------
        point: a tuple that gives a point on the maze
               for the function to check
            
        direction: a tupple from the set ((1,0), (0,1), (-1,0), (0,-1)),
                   which dictates the direction for this function to check
        
        Returns
        -------
        Nothing
    
        Side effects
        ------------
        Adds a line to the matrix
        """
        temp = [2*point[0],2*point[1]]				#Creates a temporary point from the stile matrix to be used in the normal matrix
        while 0 < temp[0] < 63 and 0 < temp[1] < 63:
            if self.matrix[temp[0]][temp[1]] == 0:	#If the point is not part of the maze, make it a travelable path
                self.matrix[temp[0]][temp[1]] = 1
                temp = [temp[0] + direction[0], temp[1] + direction[1]] #Moves the line one forward in the given direction
            else:
                break	#ends the while statement when the line reaches a "1" in the matrix
            
 
    def line_find(self, newCoords, oldCoords):
        """Draws a line between two points
    
        Parameters
        ----------
        oldCoords: The point from which the line is drawn
        newCoords: The point to which the line travels
        
        Returns
        -------
        None
    
        Side effects
        ------------
        Adds a line between the two points in the matrix.
        """  
        if newCoords[0] != oldCoords[0]: #This logic figures out which point has a higher value, and which value is higher
            if newCoords[0] > oldCoords[0]:
                for x in range(2*oldCoords[0],2*newCoords[0]+1):	#These for statements draw from the lower point to the higher one, along the given line
                    self.matrix[x][2*newCoords[1]] = 1
            else:
                for x in range(2*newCoords[0],2*oldCoords[0]+1):
                    self.matrix[x][2*newCoords[1]] = 1
        else:
            if newCoords[1] > oldCoords[1]:
                for y in range(2*oldCoords[1],2*newCoords[1]+1):
                    self.matrix[2*newCoords[0]][y] = 1
            else:
                for y in range(2*newCoords[1],2*oldCoords[1]+1):
                    self.matrix[2*newCoords[0]][y] = 1

#To finish things off, simply initialize the program by calling maze_app()

maze_app()

# Clean quit here
print("quit")
sys.exit(0)