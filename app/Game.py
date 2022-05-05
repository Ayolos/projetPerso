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

        self.main_menu = MainMenu(self)
        self.control = ControlMenu(self)
        self.score = ScoreMenu(self)
        self.curr_menu = self.main_menu
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
        self.wall_load()
        self.player = Player(self, vec(self.playerPosition))
        self.make_ghost()
        self.connection = sqlite3.connect('bdd/score.db')

    def game_loop(self):
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
                    self.curr_menu.display_menu()
            elif self.state == 'start':
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
                self.running = False
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def wall_load(self):
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

    def make_ghost(self):
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

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
                self.state = 'playing'

    def start_game(self):
        self.display.fill(BLACK)
        self.menu.draw_text((255, 255, 0), 'Appuyer sur Espace pour lancer le jeu',
                            20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        pygame.display.update()

    def playing_events(self):
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

    def playing_update(self):
        self.player.updatePlayer()
        for ghost in self.ghost:
            ghost.updateGhost()
        for ghost in self.ghost:
            # Si le joueur touche le fantome
            if ghost.gridPosition == self.player.gridPosition:
                self.remove_life()

    def playing_game(self):
        self.display.fill(BLACK)
        self.display.blit(
            self.background, (BUFFER//2, BUFFER//2))
        self.draw_pellets()
        self.menu.draw_text((255, 255, 255), 'SCORE: {}'.format(
            self.player.curScore), 20, 60, 10)
        self.player.drawPlayer()
        for ghost in self . ghost:
            ghost.drawGhost()
        pygame.display.update()

    def remove_life(self):
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

    def draw_pellets(self):
        for pellet in self.pellets:
            pygame.draw.circle(self.display, (124, 123, 7),
                               (int(pellet.x*self.cellWidth)+self.cellWidth//2+BUFFER//2,
                                int(pellet.y*self.cellHeight)+self.cellHeight//2+BUFFER//2), 5)

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.playing = False
                self.state = 'Menu'

    def game_over_game(self):
        self.display.fill(BLACK)
        quit_text = "appuye sur echap pour revenir au menu"
        again_text = "appuye sur espace pour rejouer"
        self.menu.draw_text(RED, "GAME OVER", 35, self.DISPLAY_W//2, 100)
        self.menu.draw_text((190, 190, 190), again_text, 20,
                            self.DISPLAY_W//2, self.DISPLAY_H//2)
        self.menu.draw_text((190, 190, 190), quit_text, 20,
                            self.DISPLAY_W//2, self.DISPLAY_H//1.5)
        pygame.display.update()
