# 6.00.2x Problem Set 2: Simulating robots
# SUbmitted by Jacob Okoro

import math
import random

import pylab

import ps2_visualize
# For Python 3.6:
from ps2_verify_movement36 import testRobotMovement

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = int(width) if width > 0 else 1
        self.height = int(height) if height > 0 else 1
        self.cleanList = {} #uses list to keep track of clean tiles
    
    def getCleanList(self):
        return self.cleanList

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = int(pos.getX())
        y = int(pos.getY())
        # if not self.isPositionInRoom(pos):
        #     raise ValueError('Invalid posiiton')
        if (x, y) in self.getCleanList():
            self.cleanList[(x, y)] += 1
        else:
            self.cleanList[(x, y)] = 1


    def isTileCleaned(self, m, n=0):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        # Implemented this way to account for instances where grader passed in tuples
        # rather than integer - integers are the intended arguments required(see doc string)
        if isinstance(m, tuple):
            x, y = m
            m, n = x, y
        pos = Position(m, n)
        # an optimisation to ensure that time
        # is not wasted checking tiles outside room
        if not self.isPositionInRoom(pos):
            return False
        if not (m, n) in self.cleanList:
            return False
        return True

    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.getCleanList())


    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        pos = Position(x, y)
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if x >= 0 and y >= 0:
            if x < self.width and y < self.height:
                return True
        return False


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.position = room.getRandomPosition()
        self.speed = float(speed) if speed > 0 else 1.00
        self.direction = random.randint(0, 360)
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return int(self.direction)

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if direction >= 0 and direction <= 360:
            self.direction = int(direction)

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
        # round(pos.getX()) == roomHeight or round(pos.getX())== 0) or (round(pos.getY()) == roomWidth or round(pos.getY()) == 0
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos =  self.getRobotPosition()
        speed = self.speed
        direction = self.getRobotDirection()
        next_tile = pos.getNewPosition(direction, speed)
        if (self.room.isPositionInRoom(next_tile) == False):
            self.setRobotDirection(direction)
            direction = random.randint(0, 360)
        else:
            self.setRobotPosition(next_tile)
            self.room.cleanTileAtPosition(next_tile)

        

            


# # Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    totalTime = 0
    for trial in range(num_trials):
        time_step = 0
        room = RectangularRoom(width, height)
        robot = robot_type(room, speed)
        fraction = min_coverage*room.getNumTiles()
        while room.getNumCleanedTiles() <= fraction:
            robot.updatePositionAndClean()
            toClean = 0 if room.getNumCleanedTiles() == 1 else 1
            time_step += toClean
        totalTime += time_step
    mean = totalTime/num_trials
    return mean/num_robots
    

            

# One robot takes around 150 clock ticks to completely clean a 5x5 room.
# One robot takes around 190 clock ticks to clean 75 % of a 10x10 room.
# One robot takes around 310 clock ticks to clean 90 % of a 10x10 room.
# One robot takes around 3322 clock ticks to completely clean a 20x20 room.
# Three robots take around 1105 clock ticks to completely clean a 20x20 room.

# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 5, 5, 0.9999999, 30, StandardRobot))          #tc1
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))             #tc2
# print(runSimulation(1, 1.0, 10, 10, 0.90, 30, StandardRobot))             #tc3
# print(runSimulation(1, 1.0, 20, 20, 0.9999999999, 30, StandardRobot))     #tc4
# print(runSimulation(3, 1.0, 20, 20, 0.9999999999, 30, StandardRobot))     #tc5






# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.getRobotPosition()
        speed = self.speed
        direction = self.getRobotDirection()
        next_tile = pos.getNewPosition(direction, speed)
        if (next_tile and self.room.isPositionInRoom(next_tile) != False):
            direction = random.randint(0, 360)
            self.setRobotDirection(direction)
            self.setRobotPosition(next_tile)
            self.room.cleanTileAtPosition(next_tile)
        else:
            direction = random.randint(0, 360)
            self.setRobotDirection(direction)

        




# Uncomment this line to see your implementation of StandardRobot in action!
testRobotMovement(RandomWalkRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
























# ################################################         TEST Region  ##########################################################

# TODO: is position a number
m= 1
n = 2
pos1 = Position(m, n)
# r = RectangularRoom(5, 3)
# pos2 = Position(4, 1)
# pos3 = Position(1.9, 1.1)
# print(r.isPositionInRoom(pos3))
# r.cleanTileAtPosition(pos2)
# print(r.isTileCleaned(4, 1))
# print(r.isTileCleaned(1.9, 1.1))


room = RectangularRoom(5, 6)
# Successfully created a room of size 9
# Number of clean tiles: 0
pos = Position(5.00, 6.10)
room.cleanTileAtPosition(pos)
# print(room.isTileCleaned((0, 0)))
# room.isTileCleaned(1, 2)
# print(room.isPositionInRoom(pos))

# totalTime = 0
# for trial in range(num_trials):
#     time_step = 0
#     room = RectangularRoom(width, height)
#     robot = robot_type(room, speed)
#     fraction = min_coverage*room.getNumTiles()
#     while room.getNumCleanedTiles() <= fraction:
#         robot.updatePositionAndClean()
#         time_step +=1
#     totalTime += time_step
#     mean = time_step/num_trials
#     return mean
