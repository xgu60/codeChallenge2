
import sys

#tuples are used to represent directions
#North (0, 1), South(0, -1), West(-1, 0), East(1, 0)

#Mirror object
#setup reflection rules based on different symbols
#rules can be much more complicated as shown
class Mirror(object):
    def __init__(self, symbol):
        if symbol == '/':
            self.rule = {(1, 0) : (0, 1),    #East to North
                         (0, -1) : (-1, 0),  #South to West
                         (-1, 0) : (0, -1),  #West to South
                         (0, 1) : (1, 0)}    #North to East
        elif symbol == '\\':
            self.rule = {(1, 0) : (0, -1),   #East to South
                         (0, -1) : (1, 0),   #South to East
                         (-1, 0) : (0, 1),   #West to North
                         (0, 1) : (-1, 0)}   #North to West 
        else:
            print("please input right symbol for mirror")

    def reflect(self, direction):
        return self.rule[direction]

#Maze object
class Maze(object):
    def __init__(self, x, y):  #x, y are maze size
        self.x = x
        self.y = y
        self.mirrors = {}

    def isValidPos(self, pos): #check whether a pos in maze
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.x or pos[1] >= self.y:
            return False
        return True

    def addMirror(self, pos, mirror): #add mirror to one position
        self.mirrors[pos] = mirror

    def getMirror(self, pos): #check and get the mirror object at one position
        if pos not in self.mirrors:
            return -1
        return self.mirrors[pos]

#Laser object
class Laser(object):
    def __init__(self, startPos, startDir, maze):        
        self.startPos = startPos
        self.startDir = startDir
        self.maze = maze   
        #use set to store states (pos, dir)  
        self.states = set()  
        #use list to store each visited pos    
        self.path = []
            
    def getPath(self):
        self.move(self.startPos, self.startDir)
        return self.path

    #recursive call to move the laser
    def move(self, position, direction):
        #check the validity of position
        if  not self.maze.isValidPos(position):
            self.path.append(-1)
            return
        state = position + direction
        #check the validity of state
        if state in self.states:
            self.path.append(-2)
            return
        self.states.add(state)
        self.path.append(position)
        #update position and direction
        newPos = tuple(i + j for i, j in zip(position, direction))
        mr = self.maze.getMirror(newPos)
        if mr == -1:
            newDir = direction
        else:
            newDir = mr.reflect(direction)
        #recursive call
        self.move(newPos, newDir)

#read a txt file 
#output a laser object
def readLaserMaze(filePath):
    directions = {"N": (0, 1),    #North
                  "W" : (-1, 0),  #West
                  "S" : (0, -1),  #South
                  "E" : (1, 0)}   #East
    try:
        with open(filePath) as fp:
            line = fp.readline()
            line = line.strip()
            cnt = 1
            while line:
                if cnt == 1:
                    x, y = line.split(" ")
                    maze = Maze(int(x), int(y))
                elif cnt == 2:
                    x, y, z = line.split(" ")
                    laser = Laser((int(x), int(y)), directions[z], maze)
                else:
                    x, y, z = line.split(" ")
                    maze.addMirror((int(x), int(y)), Mirror(z))
                line = fp.readline()
                line = line.strip()
                cnt += 1
        return laser

    finally:
        fp.close()

#write to a file
def writeFile(laser, filePath):
    fp = open(filePath, "w")
    path = laser.getPath()
    if path[-1] != -1:
        fp.write("-1")
    else:
        fp.write(str(len(path) - 2))
        fp.write("\n")
        fp.write(str(path[-2][0]))
        fp.write(" ")
        fp.write(str(path[-2][1]))
    fp.close()
    

def runTest(inputFilePath, outputFilePath):
    laser = readLaserMaze(inputFilePath)
    writeFile(laser, outputFilePath)   



if __name__ == '__main__':    
    runTest(sys.argv[1], sys.argv[2])
    
