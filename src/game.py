import sys
import time

import pygame

from src.elements import Elements
from src.fog import *
from src.mobs import *
from src.tilemap import TileMap


class Game:
    def __init__(self, screen: pygame.surface.Surface):
        self.WIN: pygame.surface.Surface = screen

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.tilemap: TileMap = TileMap()
        self.tilemap.load(PATHS.MAPS / "level1.csv")

        # pos, width, height, life, sprite_dict, initial_state
        self.player: Player = Player(
            pygame.math.Vector2(self.WIN.get_size()) // 2,
            PLAYER_SIZE,
            4,
            {
                "up": SpriteSheets.GreenSlime.WalkUp.get_animation(repeat=10),
                "left": SpriteSheets.GreenSlime.WalkLeft.get_animation(repeat=10),
                "right": SpriteSheets.GreenSlime.WalkRight.get_animation(repeat=10),
                "idle": SpriteSheets.GreenSlime.Idle.get_animation(repeat=10),
            },
            "idle",
        )

        self.last_time: float = time.time()  # bad
        self.dt: float = 0

        self.fog: Fog = Fog()
        self.fog.from_tilemap(self.tilemap)

        self.elements: Elements = Elements()
        self.elements.from_tilemap(self.tilemap)

        self.enemies: MobManager = MobManager()
        self.enemies.from_tilemap(self.tilemap)

        pygame.display.set_caption(NAME)

    def update(self) -> None:
        self.player.update(self.tilemap, self.dt)
        self.enemies.update(self.dt)
        self.fog.update(self.player)
        self.elements.update(self.player)

        enemy = self.enemies.check_player(self.player)
        if enemy is not None:
            self.enemies.remove(enemy)
            if self.elements.californium_count == 0:
                exit("Lost L")
            self.elements.californium_count -= 1

    def event_handler(self) -> None:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

        self.player.handle_keys(keys)

    def draw(self) -> None:
        self.WIN.fill((0, 0, 0))

        self.tilemap.draw(self.WIN)
        self.player.draw(self.WIN)
        self.elements.draw_elements(self.WIN)
        self.enemies.draw(self.WIN)
        self.fog.draw(self.WIN)
        self.elements.draw_labels(self.WIN)

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
