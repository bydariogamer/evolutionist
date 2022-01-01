from operator import attrgetter
import sys
from itertools import cycle

import pygame

import src.mobs
from src.data import FPS, BACKGROUND, PATHS, W, H
from src.utils import text, load_json
from src.spritesheet import SpriteSheet
from src.button import Button
from src.game import Game


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

    def stop(self):
        self.running = False


class MainMenu(Menu):
    TITLE = text("EVOLUTIONIST", (200, 30, 30), 150)
    AUTHORS = text("by Emc235 & bydariogamer", (250, 40, 40), 30)

    def __init__(
            self,
            screen: pygame.Surface,
            clock: pygame.time.Clock,
            buttons: Button = None,
    ):
        if buttons is None:
            buttons = [
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
    def __init__(
            self,
            screen: pygame.Surface,
            clock: pygame.time.Clock,
            buttons: Button = None,
    ):
        if buttons is None:
            buttons = [
                Button(
                    (W / 2 - 300, H / 2, 600, 100),
                    color=(100, 100, 250),
                    label="CONTINUE",
                ),
                Button(
                    (W / 2 - 300, H / 2 + 130, 600, 100),
                    color=(100, 100, 250),
                    label="EXIT",
                    on_click=[Button.put_exit]
                )
            ]
        super().__init__(screen, clock, buttons)
        darken_surface = pygame.Surface(screen.get_size())
        darken_surface.set_alpha(200)
        self.screen.blit(darken_surface, (0, 0))

    def handle_events(self, events=None):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.stop()
            for button in sorted(self.buttons, key=attrgetter("rect.right")):
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].rect.collidepoint(event.pos):
                    self.stop()

    def draw(self):
        self.screen.blit(text("PAUSE", (200, 20, 0), 120), (400, 200))
        for button in sorted(self.buttons, key=attrgetter("rect.left")):
            button.draw(self.screen)
        pygame.display.update()


class ShopMenu(Menu):
    PRICES = {
            "ICE_SPIT": 50,
            "ELECTRIC_SPIT": 100,
            "FIRE_SPIT": 200,
            "GIGANTIC": 400,
            "RETROTRANSCRIPTASE": 300,
        }

    def __init__(
            self,
            screen: pygame.Surface,
            clock: pygame.time.Clock,
            player: src.mobs.Player,
            buttons: Button = None,
    ):
        self.player = player
        if buttons is None:
            buttons = [
                Button(
                    (0, H / 2, 600, 100),
                    color=(100, 100, 250),
                    label="CONTINUE",
                ),
                Button(
                    (0, H / 2 + 130, 600, 100),
                    color=(100, 100, 250),
                    label="EXIT",
                    on_click=[Button.put_exit]
                )
            ]
        super().__init__(screen, clock, buttons)