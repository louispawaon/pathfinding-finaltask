import pygame, sys, random, math
from tkinter import messagebox, Tk
import time

size = (width, height) = 640, 480

pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("A* Pathfinding")
clock = pygame.time.Clock()

cols, rows = 64, 48


grid = []
openSet, closeSet = [], []
path = []

w = width//cols
h = height//rows

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        
    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
            
def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[0][0]
end = grid[cols - cols//2][rows - cols//4]

openSet.append(start)

def close():
    pygame.image.save(win, "AStar_End.png")
    pygame.quit()
    sys.exit()

def main():
    t1_start=0
    t2_start=0
    totaltiles=1
    pathlength=1
    flag = False
    noflag = True
    startflag = False

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:  
                   if event.button in (1, 3): 
                      clickWall(pygame.mouse.get_pos(), event.button==1)
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:  
                    clickWall(pygame.mouse.get_pos(), event.buttons[0]) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.image.save(win, "AStar_Start.png")
                    t1_start= time.time()
                    startflag = True

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]
                
                if current == end:
                    temp = current
                    while temp.prev:
                        pathlength+=1
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Total Tiles Checked:",totaltiles)
                        print("Path Length:",pathlength)
                        print("Done")
                        print("Executed Time",time.time()-t1_start)
                        
                    elif flag:
                        continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)
                    
                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)
                            totaltiles+=1
                        
                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current
                            
            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                #t2_start=time.time()
                spot = grid[i][j]
                spot.show(win, (255, 255, 255))
                if flag and spot in path:
                    spot.show(win, (25, 120, 250))
                elif spot in closeSet:
                    spot.show(win, (255, 0, 0))
                elif spot in openSet:
                    spot.show(win, (0, 255, 0))
                try:
                    if spot == end:
                        spot.show(win, (0, 120, 255))
                except Exception:
                    pass
                
        pygame.display.flip()
        
        
main()


