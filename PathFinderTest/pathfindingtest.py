import time
import os

list = [
    ['#','#','#','#','#','#','#','#','#','#'],  # I
    ['#','x','-','#','#','-','-','-','#','#'],  # I
    ['#','#','-','#','#','-','#','-','#','#'],  # Y
    ['#','-','-','#','-','-','#','-','#','#'],  # I
    ['#','-','#','#','-','#','#','-','-','#'],  # y
    ['#','-','-','-','-','#','#','#','x','#'],  # I
    ['#','#','#','#','#','#','#','#','#','#'],  #\/
]   # --------------------x---------X-------->

def searchx():
    x = 2
    xlist = []
    for rows in range(6):   #y
        for items in range(9): #x
            if x <= 0:
                break
            if list[rows][items] == 'x':
                x = x-1
                xlist.append([items,rows])
        if x <= 0:
            break
    return xlist[0][0],xlist[0][1],xlist[1][0],xlist[1][1]

x1,y1,x2,y2 = searchx()
killswitch = False

print(x1,x2)
print(y1,y2)
def maze(x,y,sinput=None):
    if sinput != None:
        list[y][x] = sinput
    return list[y][x]

def showmaze():
    print('Maze:')
    for row in list:
        print(row)

def check(positionx,positiony):
    global killswitch
    if killswitch == True:
        return None
    x = positionx   # x = 1
    y = positiony   # y = 1

    pathpoints = [[x,y]]
    #allpaths = []
    for point in pathpoints:
        above = True
        right = True
        under = True
        left = True
        ux,uy = int(point[0]),int(point[1])-1
        rx,ry = int(point[0])+1,int(point[1])
        dx,dy = int(point[0]),int(point[1])+1
        lx,ly = int(point[0])-1,int(point[1])

        if maze(ux,uy) == 'x' or maze(rx,ry) == 'x' or maze(dx,dy) == 'x' or maze(lx,ly) == 'x':
            return 'Found!'


        if maze(ux,uy) == '-':
            above = False
            #check(x,y-1)
            pathpoints.append([ux, uy])
            maze(ux, uy, 'O')

        if maze(rx,ry) == '-':
            right = False
            #check(x+1,y)
            pathpoints.append([rx,ry])
            maze(rx ,ry, 'O')
            #allpaths.append(f'x{}y{}')

        if maze(dx,dy) == '-':
            under = False
            #check(x,y+1)
            pathpoints.append([dx,dy])
            maze(dx, dy, 'O')

        if maze(lx, ly) == '-':
            left = False
            #check(x-1,y)
            pathpoints.append([lx,ly])
            maze(lx, ly, 'O')

        maze(point[0],int(point[1]),'G')
        #allpaths.append([point[0],int(point[1])])
        os.system('cls')
        showmaze()
        print('PathPoints:', pathpoints)
        #print('AllPaths:', allpaths)
        time.sleep(0.1)
    #check(x,y)
    return above, right, under, left

def go():
    x,y = x1,y1

    above, right, under, left = check(x,y)
    print(above, right, under, left)
    #if above==False:
    #    check(x,y-1)
    #if right==False:
    #    check(x+1,y)
    #if under==False:
    #    check(x,y+1)
    #if left==False:
    #    check(x-1,y)
    #print(check(2,1))



#go()
print(check(x1,y1))
