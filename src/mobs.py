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
    SPEED = 5

    def __init__(
        self,
        pos: pygame.math.Vector2,
        size: Tuple[int, int],
        life: int,
        sprite_dict: dict,
        initial_state: ...,
    ):
        super().__init__(pos, *size, life, sprite_dict, initial_state)

    def handle_keys(self, keys: Sequence[bool]):
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        if left and not (right or up or down):
            self.state = "left"
            self.vel.x = -self.SPEED
        elif right and not (left or up or down):
            self.state = "right"
            self.vel.x = self.SPEED
        elif up and not (down or left or right):
            self.state = "up"
            self.vel.y = -self.SPEED
        elif down and not (up or left or right):
            self.vel.y = self.SPEED

    def update(self, tilemap: "TileMap", dt):
        if self.vel.x == 0 == self.vel.y:
            self.state = "idle"
            return

        xc = self.vel.x * dt  # changes
        yc = self.vel.y * dt
        ox = self.rect.x  # old position to calc displacement
        oy = self.rect.y

        # x axis
        self.rect.x += xc

        if self.vel.x != 0:
            of = tilemap.offset
            for (x, y) in tilemap.empty_tiles:
                if self.rect.colliderect([x + of.x, y + of.y, *TILE_SIZE]):
                    if self.vel.x > 0:  # moving right
                        self.rect.right = x + of.x
                    else:  # moving left
                        self.rect.x = x + of.x + TL_W
                    break
            displacement = self.rect.x - ox
            self.rect.x = ox
            tilemap.offset.x -= displacement

        # y axis
        self.rect.y += yc

        if self.vel.y != 0:
            of = tilemap.offset
            for (x, y) in tilemap.empty_tiles:
                if self.rect.colliderect([x + of.x, y + of.y, *TILE_SIZE]):
                    if self.vel.y < 0:  # moving up
                        self.rect.y = y + of.y + TL_H
                    else:  # moving down
                        self.rect.bottom = y + of.y
                    break
            displacement = self.rect.y - oy
            self.rect.y = oy
            tilemap.offset.y -= displacement

        self.vel *= 0
