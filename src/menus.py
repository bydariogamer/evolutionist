from operator import attrgetter
import sys
from itertools import cycle

import pygame


from src.data import FPS, BACKGROUND, PATHS
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
    TITLE = text("EVOLUTIONIST", (200, 30, 30), 150)
    AUTHORS = text("by Emc235 & bydariogamer", (250, 40, 40), 30)

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, buttons):
        super().__init__(screen, clock, buttons)
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
        data = load_json(PATHS.SPRITESHEETS / "slime-green-right.json")
        frames = [pygame.transform.scale(
            sheet.clip(data["frames"][str(i)]), (300, 300)
        ).convert_alpha() for i in range(1, 9)]
        self.animation = cycle(
            frames
        )
        self.animation_limiter = cycle(range(4))
        self.last_anim = next(self.animation)

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        self.screen.blit(self.TITLE, (10, 30))
        self.screen.blit(self.AUTHORS, (50, 180))
        if not next(self.animation_limiter):
            self.last_anim = next(self.animation)
        self.screen.blit(self.last_anim, (800, 250))
        for button in sorted(self.buttons, key=attrgetter("rect.left")):
            button.draw(self.screen)
        pygame.display.update()


class PauseMenu(Menu):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, buttons):
        super().__init__(screen, clock, buttons)
