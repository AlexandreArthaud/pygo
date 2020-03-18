import sys
import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption('Go')

import constants
import utils
from menu import Menu
from board import Board
from game import Game

def main():
    screen = pygame.display.set_mode((constants.DIMENSIONS.window_width, constants.DIMENSIONS.window_height))
    menu = Menu(screen)

    pygame.mixer.music.load("assets/music/background.wav")
    pygame.mixer.music.play()

    # main game loop
    while True:
        choice = menu.run()
        constants.DIMENSIONS.resize(choice)
        pygame.display.set_mode((constants.DIMENSIONS.window_width, constants.DIMENSIONS.window_height))

        board = None
        if choice == constants.GameChoice.NINE_BY_NINE_GOBAN:
            board = Board(constants.GameChoice.NINE_BY_NINE_GOBAN)
        elif choice == constants.GameChoice.THIRTEEN_BY_THIRTEEN_GOBAN:
            board = Board(constants.GameChoice.THIRTEEN_BY_THIRTEEN_GOBAN)
        elif choice == constants.GameChoice.NINETEEN_BY_NINETEEN_GOBAN:
            board = Board(constants.GameChoice.NINETEEN_BY_NINETEEN_GOBAN)

        if board:
            game = Game(screen, board)
            menu.set_menu(game.run())
            #game_results = Results(screen, game.run())
            #game_results.run()

if __name__ == "__main__":
    main()
