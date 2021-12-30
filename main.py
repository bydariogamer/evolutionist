import pygame


pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()


def run():

    from src.game import Game

    game = Game(screen, clock)
    game.run()


if __name__ == "__main__":
    run()
