import pygame


pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()


def run():
    from src.menus import MainMenu
    from src.button import Button
    from src.game import Game
    from src.data import H

    MainMenu(
        screen,
        clock,
        [
            Button(
                (0, H / 2, 600, 100),
                color=(100, 100, 250),
                label="PLAY",
                on_click=[lambda _: Game(screen, clock).run()]
            ),
            Button(
                (0, H / 2 + 130, 600, 100),
                color=(100, 100, 250),
                label="EXIT",
                on_click=[Button.put_exit]
            )
        ]
    ).loop()


if __name__ == "__main__":
    run()
