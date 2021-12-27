from itertools import cycle
from src.data import *
from typing import *  # shush
import pygame
import math


class Mob:
    def __init__(self, pos, width, height, life, animation_dict, initial_state):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.life = life
        self.animation_dict = animation_dict
        self.state = initial_state
        self.vel = pygame.Vector2(0)

    def draw(self, surface: pygame.Surface):
        surface.blit(next(self.animation_dict[self.state]), self.pos)

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        # todo: check collisions in X axis

        self.pos.y += self.vel.y * dt
        # todo: check collision in Y axis

        """
        if not ground_under_its_feet:
        vel.y += some_gravity_value
        """

    def hurt(self, damage):
        self.life -= damage
        if self.life < 0:
            self.life = 0

    def kill(self):
        self.life = 0

    def change_state(self, new_state):
        self.state = new_state

    @property
    def alife(self):
        return bool(self.life)

    @property
    def pos(self):
        return pygame.Vector2(self.rect.topleft)

    @pos.setter
    def pos(self, value):
        self.rect.topleft = value

    @property
    def is_falling(self):
        return self.vel.y < 0

    @property
    def is_on_ground(self):
        return self.vel.y == 0


class Monster(Mob):
    def __init__(self, pos, width, height, life, sprite_dict, initial_state):
        super().__init__(pos, width, height, life, sprite_dict, initial_state)


class Player(Mob):
    SPEED = 2

    def __init__(
            self,
            pos: pygame.math.Vector2,
            width: int,
            height: int,
            life: int,
            sprite_dict: dict,
            initial_state: ...
    ):
        super().__init__(pos, width, height, life, sprite_dict, initial_state)

    def handle_keys(self, keys: Sequence[bool]):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.state = "left"
            self.vel.x = -self.SPEED
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.state = "right"
            self.vel.x = self.SPEED
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.state = "up"
            self.vel.y = -self.SPEED
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel.y = self.SPEED

    def update(self, tilemap: "TileMap", dt):
        self.rect.x += self.vel.x * dt

        if self.vel.x == 0 == self.vel.y:
            self.state = "idle"
            return

        if self.vel.x != 0:
            of = tilemap.offset
            for (x, y) in tilemap.empty_tiles:
                if self.rect.colliderect([x + of.x, y + of.y, *TILE_SIZE]):
                    print(True)
                    if self.vel.x > 0:  # moving right
                        self.rect.x = x + of.x
                    else:  # moving left
                        self.rect.x = x + of.x + TL_W
                    break

        self.rect.y += self.vel.y * dt
        # todo: check collision in Y axis

        self.vel *= 0
