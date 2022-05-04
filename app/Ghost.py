import pygame
import random
from  settings  import  *

class Ghost:
    def __init__(self, app, position, num):
        self.app = app
        self.gridPosition = position
        self.startPosition = [position.x, position.y]
        self.pixelPosition = self.get_pixelPosition()
        self.radius = int(self.app.cellWidth//2.3)
        self.num = num
        self.color = self.set_color()
        self.dir = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.gridPosition:
            self.pixelPosition += self.dir * self.speed
            if self.time_to_move():
                self.move()

        self.gridPosition[0] = (self.pixelPosition[0]-TOP_BOTTOM_BUFFER +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridPosition[1] = (self.pixelPosition[1]-TOP_BOTTOM_BUFFER +
                            self.app.cellHeight//2)//self.app.cellHeight+1

    def draw(self):
        pygame.draw.circle(self.app.display, self.color,
                           (int(self.pixelPosition.x), int(self.pixelPosition.y)), self.radius)

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
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

    def time_to_move(self):
        if int(self.pixelPosition.x+TOP_BOTTOM_BUFFER//2) % self.app.cellWidth == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixelPosition.y+TOP_BOTTOM_BUFFER//2) % self.app.cellHeight == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.dir = self.get_random_dir()
        if self.personality == "slow":
            self.dir = self.get_path_dir(self.target)
        if self.personality == "speedy":
            self.dir = self.get_path_dir(self.target)
        if self.personality == "scared":
            self.dir = self.get_path_dir(self.target)

    def get_path_dir(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.gridPosition[0]
        ydir = next_cell[1] - self.gridPosition[1]
        return  vec ( xdir , ydir )

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.gridPosition.x), int(self.gridPosition.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
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
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_dir(self):
        while True:
            num  =  random.randint( - 2 , 1 )
            if num == -2:
                x_dir , y_dir  =  1 , 0
            elif num == -1:
                x_dir , y_dir  =  0 , 1
            elif num == 0:
                x_dir , y_dir  =  - 1 , 0
            else:
                x_dir , y_dir  =  0 , - 1
            next_pos = vec(self.gridPosition.x + x_dir, self.gridPosition.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return  vec ( x_dir , y_dir )

    def get_pixelPosition(self):
        return vec((self.gridPosition.x*self.app.cellWidth)+TOP_BOTTOM_BUFFER//2+self.app.cellWidth//2,
                   (self.gridPosition.y*self.app.cellHeight)+TOP_BOTTOM_BUFFER//2 +
                   self.app.cellHeight//2)

    def set_color(self):
        if self.num == 0:
            return (43, 78, 203)
        if self.num == 1:
            return (197, 200, 27)
        if self.num == 2:
            return (189, 29, 29)
        if self.num == 3:
            return (215, 159, 33)

    def set_personality(self):
        if self.num == 0:
            return "speedy"
        elif self.num == 1:
            return "slow"
        elif self.num == 2:
            return "random"
        else:
            return "scared"