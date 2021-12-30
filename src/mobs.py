from itertools import cycle
import src.tilemap as tmx  # i have no idea of there is anything package with that name ¯\_(ツ)_/¯
from src.utils import *
from src.data import *
from typing import *  # shush
import random
import pygame
import math


rand = random.random
CHANCE_FOR_MOB = 0.97
is_mob = (lambda: rand() > CHANCE_FOR_MOB)


class Mob:
    def __init__(self, pos, width, height, life, animation_dict, initial_state):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.life = life
        self.animation_dict = animation_dict
        self.state = initial_state
        self.vel = pygame.Vector2(0)

    def draw(self, surface: pygame.Surface):
        surface.blit(next(self.animation_dict[self.state]), self.pos)

    def update(self, tilemap: "TileMap", dt):
        # changes
        xc = self.vel.x * dt
        yc = self.vel.y * dt
        # old position to calc displacement
        ox = self.rect.x
        oy = self.rect.y

        # x axis
        self.rect.x += xc

        if self.vel.x != 0:
            of = tilemap.offset
            for (x, y, w, h) in tilemap.empty_tiles:
                if self.rect.colliderect([x + of.x, y + of.y, *TILE_SIZE]):
                    self.rect.x = ox
                    break

        # y axis
        self.rect.y += yc

        if self.vel.y != 0:
            of = tilemap.offset
            for (x, y, w, h) in tilemap.empty_tiles:
                if self.rect.colliderect([x + of.x, y + of.y, *TILE_SIZE]):
                    self.rect.y = oy
                    break

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
        return pygame.math.Vector2(self.rect.topleft)


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

    def check_enemies(self, enemies: "MobManager", pos: pygame.math.Vector2) -> Optional["Monster"]:
        off = enemies.tm.offset  # quality so shush
        for en in enemies:
            rr = pygame.Rect(en.rect)
            rr.topleft += off
            if self.pos.distance_squared_to(rr.topleft) < 200 * 200 and rr.collidepoint(pos):
                return en

    def update(self, tilemap: "TileMap", dt):
        if self.vel.x == 0 == self.vel.y:
            self.state = "idle"
            return

        ox = self.rect.x
        oy = self.rect.y

        super().update(tilemap, dt)

        displacement = self.rect.x - ox
        self.rect.x = ox
        tilemap.offset.x -= displacement

        displacement = self.rect.y - oy
        self.rect.y = oy
        tilemap.offset.y -= displacement

        self.vel *= 0


class Monster(Mob):
    SPEED = 2

    def move(self, tilemap: tmx.TileMap, dt=1):
        right = self.state == "right"

        if right:
            self.rect.x += self.SPEED * dt
        else:
            self.rect.x -= self.SPEED * dt

        for tile in tilemap.empty_tiles:
            if tile is None: continue
            if self.rect.colliderect(tile):
                if right:
                    self.state = "left"
                    self.rect.right = tile.left
                else:
                    self.state = "right"
                    self.rect.left = tile.right
                break


class MobManager(List[Monster]):  # karen style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def good_start(self, player):
        """
        it removes teh enemies from the grid if they are too close to the player
        :param player:
        :return:
        """
        off = self.tm.offset
        max_distance = 200
        for i in sorted(range(len(self)), reverse=True):
            en = self[i]
            rr = pygame.Rect(en.rect)
            rr.topleft += off
            if pygame.math.Vector2(rr.center).distance_to(player.rect.center) < max_distance:
                self.pop(i)

    def from_tilemap(self, tilemap: tmx.TileMap):
        self.tm = tilemap
        self.clear()
        for i, row in enumerate(self.tm):
            for j, tile in enumerate(row):
                if tile in tmx.CODE:
                    if is_mob():
                        rep = 7
                        self.append(Monster((j*TL_W, i*TL_H), *SCIENTIST_SIZE, 4, {
                                        "right": SpriteSheets.Scientist.WalkRight.get_animation(repeat=rep),
                                        "left": SpriteSheets.Scientist.WalkLeft.get_animation(repeat=rep)
                                    }, "left" if rand() > 0.499999999999 else "right"
                                )
                        )

    def draw(self, surface: pygame.surface.Surface):
        o = self.tm.offset
        for en in self:
            pp = pygame.Rect(en.rect)
            en.rect.topleft += o
            en.draw(surface)
            en.rect = pp

    def update(self, dt=1):
        for en in self:
            en.move(self.tm, dt)

    def check_player(self, player: Player) -> Optional[Monster]:
        o = self.tm.offset
        for en in self:
            pp = pygame.Rect(en.rect)
            if player.rect.colliderect((pp.topleft + o, SCIENTIST_SIZE)):
                return en
        return None
