import pygame
vec  =  pygame . math . Vector2

TOP_BOTTOM_BUFFER = 50
PLAYER_COLOUR = (190, 194, 15)
WIDTH, HEIGHT = 610, 670

class Player:
    def __init__(self, app, position):
        self.app = app
        self.startPosition = [position.x, position.y]
        self.gridPosition = position
        self.pixelPosition = self.get_pixelPosition()
        self.dir = vec(0, 0)
        self.stockDir = None
        self.moove = True
        self.curScore = 0
        self.speed = 2
        self.life = 3

    def update(self):
        if self.moove:
            self.pixelPosition += self.dir*self.speed
        if self.time_to_move():
            if self.stockDir != None:
                self.dir = self.stockDir
            self.moove = self.can_move()
        # Setting grid position in reference to pix pos
        self.gridPosition[0] = (self.pixelPosition[0]-TOP_BOTTOM_BUFFER +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridPosition[1] = (self.pixelPosition[1]-TOP_BOTTOM_BUFFER +
                            self.app.cellHeight//2)//self.app.cellHeight+1
        if  self . on_coin ():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.app.display, PLAYER_COLOUR, (int(self.pixelPosition.x),
                                                            int(self.pixelPosition.y)), self.app.cellWidth//2-2)

        # Drawing player life
        for x in range(self.life):
            pygame.draw.circle(self.app.display, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

    def  on_coin ( self ):
        if self.gridPosition in self.app.pellets:
            if int(self.pixelPosition.x+TOP_BOTTOM_BUFFER//2) % self.app.cellWidth == 0:
                if self.dir == vec(1, 0) or self.dir == vec(-1, 0):
                    return True
            if int(self.pixelPosition.y+TOP_BOTTOM_BUFFER//2) % self.app.cellHeight == 0:
                if self.dir == vec(0, 1) or self.dir == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.pellets.remove(self.gridPosition)
        self.curScore += 1

    def move(self, dir):
        self.stockDir = dir

    def get_pixelPosition(self):
        return vec((self.gridPosition[0]*self.app.cellWidth)+TOP_BOTTOM_BUFFER//2+self.app.cellWidth//2,
                   (self.gridPosition[1]*self.app.cellHeight) +
                   TOP_BOTTOM_BUFFER//2+self.app.cellHeight//2)

    def time_to_move(self):
        if int(self.pixelPosition.x+TOP_BOTTOM_BUFFER//2) % self.app.cellWidth == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixelPosition.y+TOP_BOTTOM_BUFFER//2) % self.app.cellHeight == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.gridPosition+self.dir) == wall:
                return False
        return True