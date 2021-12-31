import pygame


pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()


def run():
    from src.menus import MainMenu

    MainMenu(
        screen,
        clock,
    ).loop()


if __name__ == "__main__":
    run()
