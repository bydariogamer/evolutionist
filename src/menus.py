from operator import attrgetter
import sys
from itertools import cycle

import pygame

import main
from game import Game
from src.data import FPS, BACKGROUND, W, H, PLAYER_SIZE, PATHS
from src.button import Button
from src.utils import text, load_json
from src.spritesheet import SpriteSheet


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


class MainMenu(Menu):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, buttons):
        super().__init__(screen, clock, buttons)
        self.title = text("EVOLUTIONIST", (200, 30, 30), 150)
        self.authors = text("by Emc235 & bydariogamer", (250, 40, 40), 30)
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
        data = load_json(PATHS.SPRITESHEETS / "slime-green-right.json")

        frame1 = pygame.transform.scale(
            sheet.clip(data["frames"]["1"]), (300, 300)
        ).convert_alpha()
        frame2 = pygame.transform.scale(
            sheet.clip(data["frames"]["2"]), (300, 300)
        ).convert_alpha()
        frame3 = pygame.transform.scale(
            sheet.clip(data["frames"]["3"]), (300, 300)
        ).convert_alpha()
        frame4 = pygame.transform.scale(
            sheet.clip(data["frames"]["4"]), (300, 300)
        ).convert_alpha()
        frame5 = pygame.transform.scale(
            sheet.clip(data["frames"]["5"]), (300, 300)
        ).convert_alpha()
        frame6 = pygame.transform.scale(
            sheet.clip(data["frames"]["6"]), (300, 300)
        ).convert_alpha()
        frame7 = pygame.transform.scale(
            sheet.clip(data["frames"]["7"]), (300, 300)
        ).convert_alpha()
        frame8 = pygame.transform.scale(
            sheet.clip(data["frames"]["8"]), (300, 300)
        ).convert_alpha()

        self.animation = cycle(
            [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8]
        )
        self.animation_limiter = cycle(range(4))
        self.last_anim = next(self.animation)

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        self.screen.blit(self.title, (10, 30))
        self.screen.blit(self.authors, (50, 180))
        if not next(self.animation_limiter):
            self.last_anim = next(self.animation)
        self.screen.blit(self.last_anim, (800, 250))
        for button in sorted(self.buttons, key=attrgetter("rect.left")):
            button.draw(self.screen)
        pygame.display.update()


mainmenu = MainMenu(
    main.screen,
    main.clock,
    [
        Button(
            (0, H / 2, 600, 100),
            color=(100, 100, 250),
            label="PLAY",
            on_click=[lambda _: Game(main.screen, main.clock).run()]
        ),
        Button(
            (0, H / 2 + 130, 600, 100),
            color=(100, 100, 250),
            label="EXIT",
            on_click=[Button.put_exit]
        )
    ]
)

if __name__ == "__main__":
    mainmenu.loop()
