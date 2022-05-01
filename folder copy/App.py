import pygame
import sys
import copy
import sqlite3

from Player import *
from  Ghost  import  *


pygame . init ()
vec  =  pygame . math . Vector2

# display settings
WIDTH, HEIGHT = 610, 670

TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLLARS  =  28

# color settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

class  App :
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.AppRunning = True
        self.state = 'start'
        self.cellWidth = MAZE_WIDTH//COLS
        self.cellHeight = MAZE_HEIGHT//ROWS
        self.walls = []
        self.pellets = []
        self.ghost = []
        self.ghostPosition = []
        self.playerPosition = None
        self.wall_load()
        self.player = Player(self, vec(self.playerPosition))
        self.make_ghost()
        self.connection = sqlite3.connect('score.db')

    #fonction qui permets de lancer le jeux
    def run(self):
        while self.AppRunning:
            if self.state == 'start':
                self.start_events()
                self.start_game()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_game()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_game()
            else:
                self.AppRunning = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
    

    def draw_text(self, words, display, postiontion, size, color, font_name, centered=False):
        font  =  pygame.font.SysFont( font_name , size )
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            postiontion[0] = postiontion[0]-text_size[0]//2
            postiontion[1] = postiontion[1]-text_size[1]//2
        display.blit(text, postiontion)

    def wall_load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # fonction qui va ouvrir le fichier walls.txt
        # et interpreter le fichier pour dessiner les murs
        with open("walls.txt", 'r') as file:
            for yCount, line in enumerate(file):
                for xCount, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xCount, yCount))
                    elif char == "C":
                        self.pellets.append(vec(xCount, yCount))
                    elif char == "P":
                        self.playerPosition = [xCount, yCount]
                    elif char in ["2", "3", "4", "5"]:
                        self.ghostPosition.append([xCount, yCount])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xCount*self.cellWidth, yCount*self.cellHeight,
                                                                  self.cellWidth, self.cellHeight))

    def make_ghost(self):
        for xCount, position in enumerate(self.ghostPosition):
            self.ghost.append(Ghost(self, vec(position), xCount))

    def reset(self):
        self.player.life = 3
        self.player.curScore = 0
        self.player.gridPosition = vec(self.player.startPosition)
        self.player.pixelPosition = self.player.get_pixelPosition()
        self.player.dir *= 0
        for  ghost  in  self . ghost :
            ghost.gridPosition = vec(ghost.startPosition)
            ghost.pixelPosition = ghost.get_pixelPosition()
            ghost.dir *= 0

        self.pellets = []
        with open("walls.txt", 'r') as file:
            for yCount, line in enumerate(file):
                for xCount, char in enumerate(line):
                    if char == 'C':
                        self.pellets.append(vec(xCount, yCount))
        self.state = "playing"


########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.AppRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_game(self):
        self.display.fill(BLACK)
        self.draw_text('Appuyer sur espace pour lancer le jeu', self.display, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)

        pygame.display.update()

########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.AppRunning = False
            if  event . type  ==  pygame . KEYDOWN :
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for  ghost  in  self . ghost :
            ghost.update()

        for  ghost  in  self . ghost :
            if ghost.gridPosition == self.player.gridPosition:
                self.remove_life()

    def playing_game(self):
        self.display.fill(BLACK)
        self.display.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_pellets()
        self.draw_text('SCORE: {}'.format(self.player.curScore),
                       self.display, [60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for  ghost  in  self . ghost :
            ghost.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.life -= 1
        if self.player.life == 0:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (score) VALUES(?)", (self.player.curScore,))
            self.connection.commit()
            self.state = "game over"
        else:
            self.player.gridPosition = vec(self.player.startPosition)
            self.player.pixelPosition = self.player.get_pixelPosition()
            self.player.dir *= 0
            for  ghost  in  self . ghost :
                ghost.gridPosition = vec(ghost.startPosition)
                ghost.pixelPosition = ghost.get_pixelPosition()
                ghost.dir *= 0

    def draw_pellets(self):
        for pellet in self.pellets:
            pygame.draw.circle(self.display, (124, 123, 7),
                               (int(pellet.x*self.cellWidth)+self.cellWidth//2+TOP_BOTTOM_BUFFER//2,
                                int(pellet.y*self.cellHeight)+self.cellHeight//2+TOP_BOTTOM_BUFFER//2), 5)

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.AppRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.AppRunning = False

    def game_over_game(self):
        self.display.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.display, [WIDTH//2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.display, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.display, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()