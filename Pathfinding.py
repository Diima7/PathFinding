import pygame
import queue
import threading
import time
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 16
HEIGHT = 16
 
# This sets the margin between each cell
MARGIN = 1
 
killthread = False

grid = []
for row in range(35):
    grid.append([])
    for column in range(35):
        grid[row].append(0)  # Append a cell
                                                # 1 = Wall, 2 = StartPoint, 3 = EndPoint, 4 = Search Algorithm
for wall in range(len(grid[1])):                #  X
    grid[0][wall] = 1                           #  !
    grid[34][wall] = 1                          #  !
for wall in range(len(grid)):                   #  !
    grid[wall][0] = 1                           #  !
    grid[wall][34] = 1                          #  !
grid[2][2] = 2                                  # \/ ------------------->> Y
grid[32][32] = 3


class Main():
    def __init__(self, startpoint,endpoint=None):
        self.sp = startpoint
        self.ep = endpoint
        self.found = False
    def validate(self,blockx,blocky):
        if grid[blockx][blocky] == 0:
            return True
        elif grid[blockx][blocky] == 3:
            return True
        elif grid[blockx][blocky] == 4:
            return True
        else:
            return False

    def checkfound(self,x,y):
        if grid[x][y] == 3:
            return True
        else:
            return False

    def checkcode(self,movingstring):
        spx,spy = self.sp
        for step in movingstring:
            if step == 'U':       
                x, y = spx-1, spy
                spx,spy = x,y
            if step == 'R':       
                x, y = spx, spy+1
                spx,spy = x,y
            if step == 'D':       
                x, y = spx+1, spy
                spx,spy = x,y
            if step == 'L':       
                x, y = spx, spy-1
                spx,spy = x,y
        if grid[spx][spy] == 4:
            return False
        else:
            return True

    def move(self,movingstring):            # 1 = Wall, 2 = StartPoint, 3 = EndPoint, 4 = Search Algorithm
        spx,spy = self.sp
        algorithmnum = 4
        for step in movingstring:
            if step == 'U':         #U = UP
                x, y = spx-1, spy
                if self.validate(x,y):
                    if not self.checkfound(x,y):
                        grid[x][y] = algorithmnum
                        spx, spy = x, y
                    else:
                        print('Found Path!', movingstring)
                        self.found = True
                        return True
                else:
                    return False

            if step == 'R':         #R = RIGHT
                x, y = spx, spy+1
                if self.validate(x,y):
                    if not self.checkfound(x,y):
                        grid[x][y] = algorithmnum
                        spx,spy = x,y
                    else:
                        print('Found Path!', movingstring)
                        self.found = True
                        return True
                else:
                    return False

            if step == 'D':         #D = DOWN
                x, y = spx+1, spy
                if self.validate(x,y):
                    if not self.checkfound(x,y):
                        grid[x][y] = algorithmnum
                        spx,spy = x,y
                    else:
                        print('Found Path!', movingstring)
                        self.found = True
                        return True
                else:
                    return False

            if step == 'L':         #L = LEFT
                x, y = spx, spy-1
                if self.validate(x,y):
                    if not self.checkfound(x,y):
                        grid[x][y] = algorithmnum
                        spx,spy = x,y
                    else:
                        print('Found Path!', movingstring)
                        self.found = True
                        return True
                else:
                    return False


        return 'Valid'

    def markpath(self,movingstring):
        spx,spy = self.sp
        marknum = 5
        for step in movingstring:
            time.sleep(0.02)
            if step == 'U':       
                x, y = spx-1, spy
                grid[x][y] = marknum
                spx,spy = x,y
            if step == 'R':       
                x, y = spx, spy+1
                grid[x][y] = marknum
                spx,spy = x,y
            if step == 'D':       
                x, y = spx+1, spy
                grid[x][y] = marknum
                spx,spy = x,y
            if step == 'L':       
                x, y = spx, spy-1
                grid[x][y] = marknum
                spx,spy = x,y

    def findpath(self):                   # 1 = Wall, 2 = StartPoint, 3 = EndPoint, 4 = Search Algorithm
        global killthread
        nums = queue.Queue()
        nums.put('')
        add = ''
        while self.move(add) != True:
            if self.found:
                break
            if killthread:
                print('Stop loop')
                break
            add = nums.get()
            for move in ['U','R','D','L']:
                put = add + move
                if self.checkcode(put):
                    if self.move(put) == 'Valid':
                        nums.put(put)
        if not killthread:
            self.markpath(add)
            print('The endpoint is ' + str(len(add)) + ' Block(s) away !')



sp = 2,2
mm = Main(sp)
th = threading.Thread(target=mm.findpath)


pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [595, 595]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Pathfinding Dmitri Pe.")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            killthread = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                th.start()
    if pygame.mouse.get_pressed()[0]==True:
        # User clicks the mouse. Get the position
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
        # Set that location to one
        if grid[row][column] != 1:
            if grid[row][column] != 2:
                if grid[row][column] != 3:
                    grid[row][column] = 1
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(35):
        for column in range(35):
            color = WHITE
            if grid[row][column] == 1:
                color = BLACK

            if grid[row][column] == 2:
                color = RED

            if grid[row][column] == 3:
                color = RED

            if grid[row][column] == 4:
                color = GREEN

            if grid[row][column] == 5:
                color = YELLOW

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()