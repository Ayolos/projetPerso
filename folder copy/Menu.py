import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text((253, 0, 0), 'X', 40, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Play"
        self.startx, self.starty = self.mid_w - 100, self.mid_h + 50
        self.controlx, self.controly = self.mid_w - 100, self.mid_h + 100
        self.scorex, self.scorey = self.mid_w - 100, self.mid_h + 150
        self.exitx, self.exity = self.mid_w - 100, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset -100, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.game.draw_title('Main Menu', 150, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text((255, 255, 0), "Play", 50, self.startx, self.starty)
            self.game.draw_text((255, 255, 0), "Control", 50, self.controlx, self.controly)
            self.game.draw_text((255, 255, 0), "Score", 50, self.scorex, self.scorey)
            self.game.draw_text((255, 255, 0), "Exit", 50, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Play':
                self.cursor_rect.midtop = (self.controlx + self.offset -100, self.controly)
                self.state = 'Control'
            elif self.state == 'Control':
                self.cursor_rect.midtop = (self.scorex + self.offset -100, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.exitx + self.offset -100, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset -100, self.starty)
                self.state = 'Play'
        elif self.game.UP_KEY:
            if self.state == 'Play':
                self.cursor_rect.midtop = (self.exitx + self.offset -100, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.scorex + self.offset -100, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.controlx + self.offset -100, self.controly)
                self.state = 'Control'
            elif self.state == 'Control':
                self.cursor_rect.midtop = (self.startx + self.offset -100, self.starty)
                self.state = 'Play'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Play':
                self.game.playing = True
            elif self.state == 'Skin':
                self.game.curr_menu = self.game.skin
            elif self.state == 'Control':
                self.game.curr_menu = self.game.control
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Score':
                self.game.curr_menu = self.game.score
            elif self.state == 'Exit':
                self.game.curr_menu = quit()
            self.run_display = False

class  ControlMenu ( Menu ):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.game.draw_title('Control', 100, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text((255, 255, 0), 'But: Tuer tout les MAN et manger les PELLETS', 20, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text((255, 255, 0), 'Bouger PAN: Fleche directionnelle', 20, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 - 0)

            self.game.draw_text((245, 200, 0), 'Appuyer sur Entree pour revenir au Menu', 10, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 + 300)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
        self.run_display = False

class  ScoreMenu ( Menu ):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Skin1'


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((25, 25, 166))
            self.game.draw_title('Score', 100, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 - 150)
            cursor = self.game.app.connection.cursor()
            cursor.execute("""SELECT score FROM users ORDER BY score DESC LIMIT 5""")
            rows = cursor.fetchall()
            i = 1
            for row in rows:
                highscore = pygame.font.Font("1.ttf",45).render(str('{0}'.format(row[0])), True, (255,255,255))
                highscorerect = highscore.get_rect()
                highscorerect = highscorerect.move(self.game.DISPLAY_W / 2 - 100 , 250 + i*highscorerect.bottom)
                compteur = pygame.font.Font("1.ttf",45).render(str(i), True, (255,255,255))
                compteurrect = compteur.get_rect()
                compteurrect = compteurrect.move(self.game.DISPLAY_W / 2 - 150 , 250 + i*compteurrect.bottom)
                i = i+1
                self.game.insert_image(highscore,highscorerect)
                self.game.insert_image(compteur,compteurrect)
            self.game.draw_text((255, 255, 0), 'Appuyer sur Entree pour revenir au Menu', 10, self.game.DISPLAY_W / 2 - 100, self.game.DISPLAY_H / 2 + 300)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
        self.run_display = False