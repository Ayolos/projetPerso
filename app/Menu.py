import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.runScreenMenu = True
        self.cursor = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        self.fontName = 'police/1.TTF'
        self.fontText = 'police/Retro Gaming.ttf'
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        
    def draw_cursor(self):
        self.draw_text((253, 0, 0), 'X', 40, self.cursor.x, self.cursor.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.reset_keys()
    
    def draw_title(self, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def draw_text(self, color, text, size, x, y):
        font = pygame.font.Font(self.fontText, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.runScreenMenu = False
            if event . type == pygame.KEYDOWN:
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
    
    def insert_image(self, image, pos: tuple):
        self.game.display.blit(image, pos)

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Play"
        self.startx, self.starty = self.mid_w , self.mid_h + 50
        self.controlx, self.controly = self.mid_w , self.mid_h + 100
        self.scorex, self.scorey = self.mid_w , self.mid_h + 150
        self.exitx, self.exity = self.mid_w , self.mid_h + 200
        self.cursor.midtop = (self.startx + self.offset -100, self.starty)

    def display_menu(self):
        self.runScreenMenu = True
        while self.runScreenMenu:
            self.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.draw_title('Main Menu', 150, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.draw_text((255, 255, 0), "Play", 50, self.startx, self.starty)
            self.draw_text((255, 255, 0), "Control", 50, self.controlx, self.controly)
            self.draw_text((255, 255, 0), "Score", 50, self.scorex, self.scorey)
            self.draw_text((255, 255, 0), "Exit", 50, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.DOWN_KEY:
            if self.state == 'Play':
                self.cursor.midtop = (self.controlx + self.offset -100, self.controly)
                self.state = 'Control'
            elif self.state == 'Control':
                self.cursor.midtop = (self.scorex + self.offset -100, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor.midtop = (self.exitx + self.offset -100, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor.midtop = (self.startx + self.offset -100, self.starty)
                self.state = 'Play'
        elif self.UP_KEY:
            if self.state == 'Play':
                self.cursor.midtop = (self.exitx + self.offset -100, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor.midtop = (self.scorex + self.offset -100, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor.midtop = (self.controlx + self.offset -100, self.controly)
                self.state = 'Control'
            elif self.state == 'Control':
                self.cursor.midtop = (self.startx + self.offset -100, self.starty)
                self.state = 'Play'

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Play':
                self.game.playing = True
            elif self.state == 'Control':
                self.game.curr_menu = self.game.control
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Score':
                self.game.curr_menu = self.game.score
            elif self.state == 'Exit':
                self.game.running = False
            self.runScreenMenu = False

class  ControlMenu ( Menu ):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.runScreenMenu = True
        while self.runScreenMenu:
            self.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.draw_title('Control', 100, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2 - 150)
            self.draw_text((255, 255, 0), 'But: Tuer tout les MAN et manger les PELLETS', 20, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2 - 60)
            self.draw_text((255, 255, 0), 'Bouger PAN: Fleche directionnelle', 20, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2 - 0)
            self.draw_text((255, 255, 0), 'Vous avez 3 vies pour récupérer', 20, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2+ 60)
            self.draw_text((255, 255, 0), 'tout les PELLETS', 20, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2+ 80)

            self.draw_text((245, 200, 0), 'Appuyer sur Entree pour revenir au Menu', 10, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2 + 300)
            self.blit_screen()

    def check_input(self):
        if self.START_KEY:
            self.game.curr_menu = self.game.main_menu
        self.runScreenMenu = False

class  ScoreMenu ( Menu ):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.runScreenMenu = True
        while self.runScreenMenu:
            self.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.draw_title('Score', 100, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            cursor = self.game.connection.cursor()
            cursor.execute("""SELECT score FROM users ORDER BY score DESC LIMIT 5""")
            rows = cursor.fetchall()
            i = 1
            for row in rows:
                highscore = pygame.font.Font(self.fontName,45).render(str('{0}'.format(row[0])), True, (255,255,255))
                highscorerect = highscore.get_rect()
                highscorerect = highscorerect.move(self.game.DISPLAY_W / 2  , 250 + i*highscorerect.bottom)
                compteur = pygame.font.Font(self.fontName,45).render(str(i), True, (255,255,255))
                compteurrect = compteur.get_rect()
                compteurrect = compteurrect.move(self.game.DISPLAY_W / 2 - 50 , 250 + i*compteurrect.bottom)
                i = i+1
                self.insert_image(highscore,highscorerect)
                self.insert_image(compteur,compteurrect)
            self.draw_text((255, 255, 0), 'Appuyer sur Entree pour revenir au Menu', 10, self.game.DISPLAY_W / 2 , self.game.DISPLAY_H / 2 + 300)
            self.blit_screen()

    def check_input(self):
        if self.START_KEY:
            self.game.curr_menu = self.game.main_menu
        self.runScreenMenu = False