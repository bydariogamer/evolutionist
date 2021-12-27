from src.spritesheet import SpriteSheet
from src.tilemap import TileMap
from src.utils import *
from src.data import *
import pygame
import time
import math
import sys
import os


class Game:
    def __init__(self):
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((W, H))

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.tilemap: TileMap = TileMap()
        self.tilemap.load(PATHS.MAPS / "level1.csv")

        self.last_time: float = time.time()  # bad
        self.dt: float = 0

        pygame.display.set_caption(NAME)

    def update(self) -> None:
        pass

    def event_handler(self) -> None:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # basic world moving that can go in the player, dt is used cause slow
        off = [0, 0]
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            off[1] += 5 * self.dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            off[1] -= 5 * self.dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            off[0] += 5 * self.dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            off[0] -= 5 * self.dt
        self.tilemap.offset(off)

    def draw(self) -> None:
        self.WIN.fill((0, 0, 0))

        self.tilemap.draw(self.WIN)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.dt = time.time() - self.last_time
            self.dt *= self.FPS
            self.last_time = time.time()

            self.clock.tick(self.FPS)
            self.event_handler()  # input
            self.update()  # process
            self.draw()  # show
