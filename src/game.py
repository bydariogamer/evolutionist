import sys
import time

import pygame
import random
from typing import *

from src.button import Button
from src.collectables import Collectables
from src.data import *
from src.utils import *
from src.fog import Fog
from src.mobs import Player, Monster, MobManager
from src.tilemap import TileMap


class Game:
    def __init__(self, screen: pygame.surface.Surface, clock: pygame.time.Clock):
        self.WIN: pygame.surface.Surface = screen

        self.running: bool = True
        self.clock = clock

        self.frame_count: int = 0

        self.FPS: int = 60

        self.last_time: float = time.time()  # bad
        self.dt: float = 0
        
        self.initialize(PATHS.MAPS / "level1.csv")

        pygame.display.set_caption(NAME)

    def initialize(self, path: str):
        self.tilemap: TileMap = TileMap()
        self.tilemap.load(PATHS.MAPS / path)

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

        self.fog: Fog = Fog()
        self.fog.from_tilemap(self.tilemap)

        self.collectables: Collectables = Collectables()
        self.collectables.from_tilemap(self.tilemap)

        self.enemies: MobManager = MobManager()
        self.enemies.from_tilemap(self.tilemap)
        self.enemies.good_start(self.player)
        
        # enemy, surf, pos, vel, last_frame_to_be_alive, callable
        self.bullets: List[
            List[Union[Monster, pygame.surface.Surface, pygame.math.Vector2, pygame.math.Vector2, int, type(lambda x: None)]]
        ] = []
        
        self.DNA_count: int = 0

    @property
    def is_level_finished(self):
        return all(en.ded for en in self.enemies) and not self.collectables

    def collectable_to_dna(self, _=None):
        if self.collectables.is_eligible_for_dna:
            self.collectables.uranium_count -= 3
            self.collectables.thorium_count -= 2
            self.collectables.californium_count -= 1
            self.DNA_count += 1

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
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
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

                    # check for the DNA point system
                    x, y = event.pos
                    if x <= ELEMENT_DISPLAY_SIZE[0] * 3 and y >= H - ELEMENT_DISPLAY_SIZE[1]:
                        if x <= ELEMENT_DISPLAY_SIZE[0] * 1:
                            if self.collectables.uranium_count >= 1:
                                self.collectables.uranium_count -= 1
                                self.DNA_count += 1
                        if x <= ELEMENT_DISPLAY_SIZE[0] * 2:
                            if self.collectables.californium_count >= 1:
                                self.collectables.californium_count -= 1
                                self.DNA_count += 3
                        if x <= ELEMENT_DISPLAY_SIZE[0] * 3:
                            if self.collectables.thorium_count >= 1:
                                self.collectables.thorium_count -= 1
                                self.DNA_count += 2

        self.player.handle_keys(keys)

    def draw(self) -> None:
        self.WIN.fill((0, 0, 0))

        self.tilemap.draw(self.WIN)
        self.player.draw(self.WIN)
        self.collectables.draw_elements(self.WIN)
        self.enemies.draw(self.WIN)
        self.enemies.draw_health(self.WIN)

        for i, [enemy, surf, pos, vel, last_frame, type_, call] in sorted(enumerate(self.bullets), reverse=True):
            if last_frame == self.frame_count:
                self.bullets.pop(i)
                call()
                enemy.stop_idle()
                if enemy.ded:
                    if type_ == "electro":
                        if enemy.state in "up|down":
                            ani = random.choice([
                                SpriteSheets.Scientist.DeathAnimations.ElectrifiedRight.get_animation,
                                SpriteSheets.Scientist.DeathAnimations.ElectrifiedLeft.get_animation
                            ])(repeat=10)
                        else:
                            ani = {
                                "right": SpriteSheets.Scientist.DeathAnimations.ElectrifiedRight.get_animation,
                                "left": SpriteSheets.Scientist.DeathAnimations.ElectrifiedLeft.get_animation
                            }[enemy.state](repeat=10)
                    elif type_ == "ice":
                        if enemy.state in "up|down":
                            ani = random.choice([
                                SpriteSheets.Scientist.DeathAnimations.FreezingRight.get_animation,
                                SpriteSheets.Scientist.DeathAnimations.FreezingLeft.get_animation
                            ])(repeat=10)
                        else:
                            ani = {
                                "right": SpriteSheets.Scientist.DeathAnimations.FreezingRight.get_animation,
                                "left": SpriteSheets.Scientist.DeathAnimations.FreezingLeft.get_animation
                            }[enemy.state](repeat=10)
                    elif type_ == "fire":
                        if enemy.state in "up|down":
                            ani = random.choice([
                                SpriteSheets.Scientist.DeathAnimations.OnFireRight.get_animation,
                                SpriteSheets.Scientist.DeathAnimations.OnFireLeft.get_animation
                            ])(repeat=10)
                        else:
                            ani = {
                                "right": SpriteSheets.Scientist.DeathAnimations.OnFireRight.get_animation,
                                "left": SpriteSheets.Scientist.DeathAnimations.OnFireLeft.get_animation
                            }[enemy.state](repeat=10)
                    elif type_ == "acid":
                        if enemy.state in "up|down":
                            ani = random.choice([
                                SpriteSheets.Scientist.DeathAnimations.AcidRight.get_animation,
                                SpriteSheets.Scientist.DeathAnimations.AcidLeft.get_animation
                            ])(repeat=10)
                        else:
                            ani = {
                                "right": SpriteSheets.Scientist.DeathAnimations.AcidRight.get_animation,
                                "left": SpriteSheets.Scientist.DeathAnimations.AcidLeft.get_animation
                            }[enemy.state](repeat=10)
                    else:
                        print(f"unknown animation type '{type_}'")

                    enemy.animation_dict["ded"] = ani
                    enemy.state = "ded"
            self.WIN.blit(surf, pos)

        self.fog.draw(self.WIN)  # the fog to hid uncovered areas
        self.collectables.draw_labels(self.WIN)  # basic UI

        # DNA number count
        self.WIN.blit(Images.DNA, (ELEMENT_DISPLAY_SIZE[0]*3 + 4, H - ELEMENT_DISPLAY_SIZE[1] + 5))

        # DNA image
        self.WIN.blit(
            Fonts.pixel_font.render(number_format(self.DNA_count, 2), True, (70, 70, 70)),
            (ELEMENT_DISPLAY_SIZE[0]*3 + 4, H - ELEMENT_DISPLAY_SIZE[1] + 45)
        )

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

            self.frame_count += 1
