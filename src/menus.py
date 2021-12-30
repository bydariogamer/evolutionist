from operator import attrgetter
import sys

import pygame

import main
from game import Game
from src.data import FPS, BACKGROUND, W, H
from src.button import Button


class Menu:
    BACKGROUND = BACKGROUND

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, buttons):
        self.screen = screen
        self.clock = clock
        self.buttons = buttons
        self.dt = 0
        self.running = True

    def handle_events(self, events=None):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

            for button in sorted(self.buttons, key=attrgetter("rect.right")):
                button.handle_event(event)

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        for button in sorted(self.buttons, key=attrgetter("rect.left")):
            button.draw(self.screen)
        pygame.display.update()

    def update(self):
        self.dt = self.clock.tick(FPS)

    def loop(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.update()


mainmenu = Menu(
    main.screen,
    main.clock,
    [
        Button(
            (0, H / 2 - 100, 600, 100),
            color=(100, 100, 250),
            label="Play",
            on_click=[lambda _: Game(main.screen, main.clock).run()]
        ),
    ]
)

if __name__ == "__main__":
    mainmenu.loop()
