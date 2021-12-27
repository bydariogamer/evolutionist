from src.game import Game
import pygame


def run():
    pygame.init()
    pygame.font.init()
    pygame.display.init()

    game = Game()
    game.run()


if __name__ == '__main__':
    run()
