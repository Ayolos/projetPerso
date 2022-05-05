import pygame
import sys
import sqlite3

from Menu import *
from Player import *
from Ghost import *
from settings import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = 610, 670
        self.MAZE_WIDTH, self.MAZE_HEIGHT = self.DISPLAY_W-BUFFER, self.DISPLAY_H-BUFFER

        self.window = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.display = pygame.display.set_mode(
            ((self.DISPLAY_W, self.DISPLAY_H)))

        self.mainMenu = MainMenu(self)
        self.control = ControlMenu(self)
        self.score = ScoreMenu(self)
        self.currMenu = self.mainMenu
        self.menu = Menu(self)


        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.cellWidth = self.MAZE_WIDTH//COLS
        self.cellHeight = self.MAZE_HEIGHT//ROWS
        self.walls = []
        self.pellets = []
        self.ghost = []
        self.ghostPosition = []
        self.playerPosition = None
        self.loadWall()
        self.player = Player(self, vec(self.playerPosition))
        self.ghostInit()
        self.connection = sqlite3.connect('bdd/score.db')

    def runGame(self):
        if self.playing:
            self.run()

    def run(self):
        while self.running:
            print(self.state)
            if self.state == 'Menu':
                while self.state == 'Menu':
                    if self.playing == True:
                        self.state = "start"
                        break
                    self.currMenu.display_menu()
            elif self.state == 'start':
                self.checkStart()
                self.gameStart()
            elif self.state == 'playing':
                self.checkPlaying()
                self.updatePlaying()
                self.gamePlaying()
            elif self.state == 'game over':
                self.checkGameOver()
                self.gameOver()
            else:
                self.running = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def loadWall(self):
        self.background = pygame.image.load('image/maze.png')
        self.background = pygame.transform.scale(
        self.background, (self.MAZE_WIDTH, self.MAZE_HEIGHT))

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

    def ghostInit(self):
        for xCount, position in enumerate(self.ghostPosition):
            self.ghost.append(Ghost(self, vec(position), xCount))

    def reset(self):
        self.player.life = 3
        self.player.curScore = 0
        self.player.gridPosition = vec(self.player.startPosition)
        self.player.pixelPosition = self.player.getPosition()
        self.player.dir *= 0
        for ghost in self . ghost:
            ghost.gridPosition = vec(ghost.startPosition)
            ghost.pixelPosition = ghost.getPosition()
            ghost.dir *= 0

        self.pellets = []
        with open("walls.txt", 'r') as file:
            for yCount, line in enumerate(file):
                for xCount, char in enumerate(line):
                    if char == 'C':
                        self.pellets.append(vec(xCount, yCount))

    def checkStart(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
                self.state = 'playing'

    def gameStart(self):
        self.display.fill(BLACK)
        self.menu.draw_text((255, 255, 0), 'Appuyer sur Espace pour lancer le jeu',
                            20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        pygame.display.update()

    def checkPlaying(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event . type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.isMoove(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.isMoove(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.isMoove(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.isMoove(vec(0, 1))

    def updatePlaying(self):
        self.player.updatePlayer()
        for ghost in self.ghost:
            ghost.updateGhost()
        for ghost in self.ghost:
            # Si le joueur touche le fantome
            if ghost.gridPosition == self.player.gridPosition:
                self.looseLife()

    def gamePlaying(self):
        self.display.fill(BLACK)
        self.display.blit(
            self.background, (BUFFER//2, BUFFER//2))
        self.pelletsInit()
        self.menu.draw_text((255, 255, 255), 'SCORE: {}'.format(
            self.player.curScore), 20, 60, 10)
        self.player.drawPlayer()
        for ghost in self . ghost:
            ghost.drawGhost()
        pygame.display.update()

    def looseLife(self):
        self.player.life -= 1
        if self.player.life == 0:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (score) VALUES(?)",
                           (self.player.curScore, ))
            self.connection.commit()
            self.state = "game over"
        else:
            self.player.gridPosition = vec(self.player.startPosition)
            self.player.pixelPosition = self.player.getPosition()
            self.player.dir *= 0
            for ghost in self . ghost:
                ghost.gridPosition = vec(ghost.startPosition)
                ghost.pixelPosition = ghost.getPosition()
                ghost.dir *= 0

    def pelletsInit(self):
        for pellet in self.pellets:
            pygame.draw.circle(self.display, (124, 123, 7),
                               (int(pellet.x*self.cellWidth)+self.cellWidth//2+BUFFER//2,
                                int(pellet.y*self.cellHeight)+self.cellHeight//2+BUFFER//2), 5)

    def checkGameOver(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.playing = False
                self.state = 'Menu'

    def gameOver(self):
        self.display.fill(BLACK)
        exitText = "appuye sur echap pour revenir au menu"
        resetText = "appuye sur espace pour rejouer"
        self.menu.draw_text(RED, "GAME OVER", 35, self.DISPLAY_W//2, 100)
        self.menu.draw_text((190, 190, 190), resetText, 20,
                            self.DISPLAY_W//2, self.DISPLAY_H//2)
        self.menu.draw_text((190, 190, 190), exitText, 20,
                            self.DISPLAY_W//2, self.DISPLAY_H//1.5)
        pygame.display.update()
