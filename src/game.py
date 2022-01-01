import sys
import time

import pygame
import random
from typing import *

from src.collectables import Collectables
from src.data import *
from src.utils import *
from src.fog import Fog
from src.mobs import Player, Monster, MobManager
from src.tilemap import TileMap


class Game:
    def __init__(self, screen: pygame.surface.Surface, clock: pygame.time.Clock):
        self.screen: pygame.surface.Surface = screen

        self.running: bool = True
        self.clock = clock

        self.frame_count: int = 0

        self.FPS: int = 60

        self.last_time: float = time.time()  # bad
        self.dt: float = 0

        self.current_level: int = 0

        self.tilemap: TileMap = TileMap()
        self.player: Player = Player(
            pygame.math.Vector2(self.screen.get_size()) // 2,
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
        self.fog: Fog = Fog()
        self.collectables: Collectables = Collectables()
        self.enemies: MobManager = MobManager()

        # enemy, surf, pos, vel, last_frame_to_be_alive, callable
        self.bullets: List[
            List[Union[
                Monster, pygame.surface.Surface, pygame.math.Vector2, pygame.math.Vector2, int, type(lambda x: None)]]
        ] = []

        self.initialize()

        pygame.display.set_caption(NAME)

    def initialize(self, path: Union[str, Path] = None):
        if path is None:
            path = PATHS.MAPS / f"level{self.current_level}.csv"
        self.tilemap.load(PATHS.MAPS / path)
        self.fog.from_tilemap(self.tilemap)
        self.collectables.from_tilemap(self.tilemap)
        self.enemies.from_tilemap(self.tilemap, self.current_level)
        self.enemies.good_start(self.player)

    @property
    def is_level_finished(self):
        return all(en.ded for en in self.enemies) and not self.collectables

    def update(self) -> None:
        self.player.update(self.tilemap, self.dt)
        self.enemies.update(self.dt)
        self.fog.update(self.player)
        self.collectables.update(self.player)

        enemy = self.enemies.check_player(self.player)
        if enemy is not None and not enemy.ded:
            # TODO: make this shit do something when you die and not just say L :kekw:
            exit("Lost L GG (Get Good lmao)")

        for [enemy, surf, pos, vel, last_frame, type_, call] in self.bullets:
            pos += vel

    def event_handler(self) -> None:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # TODO: implement pause menu
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from src.menus import PauseMenu
                PauseMenu(self.screen, self.clock).loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    enemy = self.player.check_enemies(self.enemies, pygame.math.Vector2(event.pos))
                    # check if the enemy is already under attack so it is "fair"
                    for [en, surf, pos, vel, last_frame, type_, call] in self.bullets:
                        if en is enemy:
                            break
                    # add the enemy in the bullets lists
                    else:  # triggered only when the for loop didnt hit a break statement
                        if enemy is not None:
                            self.enemies.attack(enemy, self.player, self)

        self.player.handle_keys(keys)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)
        self.collectables.draw_elements(self.screen)
        self.enemies.draw(self.screen)
        self.enemies.draw_health(self.screen)

        for i, [enemy, surf, pos, vel, last_frame, type_, call] in sorted(enumerate(self.bullets), reverse=True):
            if last_frame == self.frame_count:
                self.bullets.pop(i)
                call()
                enemy.stop_idle()
                if enemy.ded:
                    animation_type = {
                                         "electric": "Electrified",
                                         "ice": "Freezing",
                                         "fire": "OnFire",
                                         "acid": "Acid"
                                     }[type_] + {
                                         "right": "Right",
                                         "left": "Left"
                                     }[enemy.state if enemy.state in {"right", "left"} else random.choice(
                        ["right", "left"])]

                    enemy.animation_dict["ded"] = getattr(SpriteSheets.Scientist.DeathAnimations,
                                                          animation_type).get_animation(repeat=10)
                    enemy.state = "ded"
            self.screen.blit(surf, pos)

        # the fog to hid uncovered areas
        self.fog.draw(self.screen)

        # DNA number count
        self.screen.blit(Images.DNA, (5, H - Images.DNA.get_size()[1] - 5))
        self.screen.blit(text(str(self.player.mutation_points), (20, 250, 20)),
                         (10 + Images.DNA.get_size()[1], H - Images.DNA.get_size()[1]))

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.dt = time.time() - self.last_time
            self.dt *= self.FPS
            self.last_time = time.time()

            self.event_handler()  # input
            self.update()  # process
            self.draw()  # show
            if self.is_level_finished:
                self.current_level += 1
                print("LEVEL ENDED")
                self.initialize()

            self.frame_count += 1
