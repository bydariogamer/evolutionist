import pygame


def run():
    pygame.init()
    pygame.font.init()
    pygame.display.init()

    screen = pygame.display.set_mode((1200, 700))

    from src.game import Game

    game = Game(screen)
    game.run()


if __name__ == "__main__":
    run()
