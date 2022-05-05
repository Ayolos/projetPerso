import pygame
import random
from  settings  import  *

class Ghost:
    def __init__(self, app, position, num):
        self.app = app
        self.gridPosition = position
        self.startPosition = [position.x, position.y]
        self.pixelPosition = self.getPosition()
        self.radius = int(self.app.cellWidth//2.3)
        self.num = num
        self.color = self.color()
        self.dir = vec(0, 0)
        self.personality = self.personality()
        self.target = None
        self.speed = self.speed()

    def updateGhost(self):
        self.target = self.isTarget()
        if self.target != self.gridPosition:
            self.pixelPosition += self.dir * self.speed
            if self.testMoove():
                self.moove()

        self.gridPosition[0] = (self.pixelPosition[0]-BUFFER +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridPosition[1] = (self.pixelPosition[1]-BUFFER +
                            self.app.cellHeight//2)//self.app.cellHeight+1

    def drawGhost(self):
        pygame.draw.circle(self.app.display, self.color,
                           (int(self.pixelPosition.x), int(self.pixelPosition.y)), self.radius)

    def speed(self):
        if self.personality in ["speed", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def isTarget(self):
        if self.personality == "speed" or self.personality == "slow":
            return self.app.player.gridPosition
        else:
            if self.app.player.gridPosition[0] > COLS//2 and self.app.player.gridPosition[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.gridPosition[0] > COLS//2 and self.app.player.gridPosition[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.gridPosition[0] < COLS//2 and self.app.player.gridPosition[1] > ROWS//2:
                return  vec ( COLS - 2,1 )
            else:
                return vec(COLS-2, ROWS-2)

    def testMoove(self):
        if int(self.pixelPosition.x+BUFFER//2) % self.app.cellWidth == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixelPosition.y+BUFFER//2) % self.app.cellHeight == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                return True
        return False

    def moove(self):
        if self.personality == "random":
            self.dir = self.getDirRandom()
        if self.personality == "slow":
            self.dir = self.getDir(self.target)
        if self.personality == "speed":
            self.dir = self.getDir(self.target)
        if self.personality == "scared":
            self.dir = self.getDir(self.target)

    def getDir(self, target):
        nextCell = self.nextCell(target)
        xdir = nextCell[0] - self.gridPosition[0]
        ydir = nextCell[1] - self.gridPosition[1]
        return  vec ( xdir , ydir )

    def nextCell(self, target):
        path = self.browsePath([int(self.gridPosition.x), int(self.gridPosition.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def browsePath(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            nextCell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if nextCell not in visited:
                                if grid[nextCell[1]][nextCell[0]] != 1:
                                    queue.append(nextCell)
                                    path.append({"Current": current, "Next": nextCell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def getDirRandom(self):
        while True:
            num  =  random.randint( - 2 , 1 )
            if num == -2:
                x , y  =  1 , 0
            elif num == -1:
                x , y  =  0 , 1
            elif num == 0:
                x , y  =  - 1 , 0
            else:
                x , y  =  0 , - 1
            nextPos = vec(self.gridPosition.x + x, self.gridPosition.y + y)
            if nextPos not in self.app.walls:
                break
        return  vec ( x , y )

    def getPosition(self):
        return vec((self.gridPosition.x*self.app.cellWidth)+BUFFER//2+self.app.cellWidth//2,
                   (self.gridPosition.y*self.app.cellHeight)+BUFFER//2 +
                   self.app.cellHeight//2)

    def color(self):
        if self.num == 0:
            return (43, 78, 203)
        if self.num == 1:
            return (197, 200, 27)
        if self.num == 2:
            return (189, 29, 29)
        if self.num == 3:
            return (215, 159, 33)

    def personality(self):
        if self.num == 0:
            return "speed"
        elif self.num == 1:
            return "slow"
        elif self.num == 2:
            return "random"
        else:
            return "scared"