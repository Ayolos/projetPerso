import pygame
import sqlite3
import random
from Menu import *
from App import *

vec  =  pygame . math . Vector2
black = (0,0,0)
blue = (25, 25, 166)
clock = pygame.time.Clock()
pygame.init()

class Game():
    def __init__(self):
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 700
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '1.TTF'
        self.font_text = 'police/Retro Gaming.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self . main_menu  =  MainMenu ( self )
        self.control = ControlMenu(self)
        self.score = ScoreMenu(self)
        self.curr_menu = self.main_menu
        self.app = App()
        

    def game_loop(self):
        if self.playing:
            self.app . run ()



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if  event . type  ==  pygame . KEYDOWN :
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_title(self, text, size, x, y ):
        font  =  pygame.font.Font(self.font_name , size )
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def draw_text(self, color, text, size, x, y ):
        font  =  pygame.font.Font(self.font_text , size )
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def insert_image(self, image, pos: tuple):
        self.display.blit(image, pos)

