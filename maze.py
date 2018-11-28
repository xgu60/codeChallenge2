
import sys

#tuples are used to represent directions
#North (0, 1), South(0, -1), West(-1, 0), East(1, 0)

#Mirror object
class Mirror(object):
    def __init__(self, symbol):
        self.symbol = symbol
        
    def reflect(self, direction):
        if self.symbol == '/':
            return direction[1], direction[0]
        else:
            return -direction[1], -direction[0]

#Maze object
class Maze(object):
    def __init__(self, x, y):  #x, y are maze size
        self.x = x
        self.y = y
        self.mirrors = {}

    def is_valid_pos(self, pos): #check whether a pos in maze
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.x or pos[1] >= self.y:
            return False
        return True

    def add_mirror(self, pos, mirror): #add mirror to one position
        self.mirrors[pos] = mirror

    def get_mirror(self, pos): #check and get the mirror object at one position
        if pos not in self.mirrors:
            return -1
        return self.mirrors[pos]

#Laser object
class Laser(object):
    def __init__(self, start_pos, start_dir, maze):        
        self.start_pos = start_pos
        self.start_dir = start_dir
        self.maze = maze   
        #use set to store states (pos, dir)  
        self.states = set()  
        #use list to store each visited pos    
        self.path = []
            
    def get_path(self):
        self.move(self.start_pos, self.start_dir)
        return self.path

    #recursive call to move the laser
    def move(self, position, direction):
        #check the validity of position
        if  not self.maze.is_valid_pos(position):
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
        mr = self.maze.get_mirror(newPos)
        if mr == -1:
            newDir = direction
        else:
            newDir = mr.reflect(direction)
        #recursive call
        self.move(newPos, newDir)
    
    def print_laserMaze(self):
        for x in range(self.maze.x):
            print("---", end="")
        print("\n")
        for y in range(self.maze.y - 1, -1 , -1):
            for x in range(self.maze.x):
                if (x, y) in self.maze.mirrors:
                    print(" " + self.maze.mirrors[(x, y)].symbol + " ", end="")
                elif (x, y) in self.path:
                    print(" * ", end="")
                else:
                    print("   ", end="")
            print("\n")
        for x in range(self.maze.x):
            print("---", end="")
        print("\n")
                

#read a txt file 
#output a laser object
def read_laserMaze(file_path):
    directions = {"N": (0, 1),    #North
                  "W" : (-1, 0),  #West
                  "S" : (0, -1),  #South
                  "E" : (1, 0)}   #East
    try:
        with open(file_path) as fp:
            line = fp.readline().strip()
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
                    maze.add_mirror((int(x), int(y)), Mirror(z))
                line = fp.readline().strip()
                cnt += 1
        return laser

    finally:
        fp.close()

#write to a file
def write_file(laser, file_path):
    fp = open(file_path, "w")
    path = laser.get_path()
    laser.print_laserMaze()    
    if path[-1] != -1:
        fp.write("-1")
    else:
        fp.write(str(len(path) - 2))
        fp.write("\n")
        fp.write(str(path[-2][0]))
        fp.write(" ")
        fp.write(str(path[-2][1]))
    fp.close()
    

def run_test(input_file_path, output_file_path):
    laser = read_laserMaze(input_file_path)
    write_file(laser, output_file_path)   



if __name__ == '__main__':    
    run_test(sys.argv[1], sys.argv[2])
    
