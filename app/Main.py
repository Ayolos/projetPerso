from Game import *

ga = Game()

while ga.running:
    ga.currMenu.display_menu()
    ga.runGame()