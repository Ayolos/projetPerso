import pygame
from  settings  import  *


class Player:
    def __init__(self, app, position):
        self.app = app
        self.startPosition = [position.x, position.y]
        self.gridPosition = position
        self.pixelPosition = self.getPosition()
        self.dir = vec(0, 0)
        self.stockDir = None
        self.moove = True
        self.curScore = 0
        self.speed = 2
        self.life = 1

    def updatePlayer(self):
        if self.moove:
            self.pixelPosition += self.dir*self.speed
        if self.testMoove():
            if self.stockDir != None:
                self.dir = self.stockDir
            self.moove = self.collisionWall()
        self.gridPosition[0] = (self.pixelPosition[0]-BUFFER +
                                self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridPosition[1] = (self.pixelPosition[1]-BUFFER +
                                self.app.cellHeight//2)//self.app.cellHeight+1
        if self . onPellets():
            self.eatPellets()

    def drawPlayer(self):
        pygame.draw.rect(self.app.display, GREEN, (int(self.pixelPosition.x) -8, int(self.pixelPosition.y)-8, 15, 15))

        for x in range(self.life):
            pygame.draw.circle(self.app.display, GREEN,
                               (30 + 20*x, 670 - 15), 7)

    def onPellets(self):
        if self.gridPosition in self.app.pellets:
            if int(self.pixelPosition.x+BUFFER//2) % self.app.cellWidth == 0:
                if self.dir == vec(1, 0) or self.dir == vec(-1, 0):
                    return True
            if int(self.pixelPosition.y+BUFFER//2) % self.app.cellHeight == 0:
                if self.dir == vec(0, 1) or self.dir == vec(0, -1):
                    return True
        return False

    def eatPellets(self):
        self.app.pellets.remove(self.gridPosition)
        self.curScore += 1

    def isMoove(self, dir):
        self.stockDir = dir

    def getPosition(self):
        return vec((self.gridPosition[0]*self.app.cellWidth)+BUFFER//2+self.app.cellWidth//2,
                   (self.gridPosition[1]*self.app.cellHeight) +
                   BUFFER//2+self.app.cellHeight//2)

    def testMoove(self):
        if int(self.pixelPosition.x+BUFFER//2) % self.app.cellWidth == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixelPosition.y+BUFFER//2) % self.app.cellHeight == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                return True

    def collisionWall(self):
        for wall in self.app.walls:
            if vec(self.gridPosition+self.dir) == wall:
                return False
        return True
