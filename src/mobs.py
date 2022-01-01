from itertools import cycle
from typing import *
import random

import pygame

import src.tilemap as tmx  # i have no idea of there is anything package with that name ¯\_(ツ)_/¯
from src.utils import *
from src.data import *



rand = random.random
CHANCE_FOR_MOB = 0.9
is_mob = (lambda: rand() > CHANCE_FOR_MOB)

MAX_HEALTH = 4

ATTACKS = {
    "electric": SpriteSheets.Bullets.electro,
    "ice": SpriteSheets.Bullets.ice,
    "fire": SpriteSheets.Bullets.fire,
    "acid": SpriteSheets.Bullets.acid
}


class Mob:  # abstract class????????
    def __init__(self, pos, width, height, life, animation_dict, initial_state):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.life = life
        self.animation_dict = animation_dict
        self.state = initial_state
        self.vel = pygame.Vector2(0)

    def draw(self, surface: pygame.Surface):
        if isinstance(self, Monster) and self.ded:
            try:
                surface.blit(self.last_image, self.pos)
                self.last_image = next(self.animation_dict[self.state])
            except StopIteration:
                pass
        else:
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
        self.mutations = {
            "ICE_SPIT": False,
            "ELECTRIC_SPIT": False,
            "FIRE_SPIT": False,
            "GIGANTIC": False,
            "RETROTRANSCRIPTASE": False,
        }
        self.mutation_points = 0

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
        max_distance = 200
        for en in enemies:
            rr = pygame.Rect(en.rect)
            rr.topleft += off
            if not en.ded and self.pos.distance_squared_to(rr.topleft) < max_distance * max_distance and rr.collidepoint(pos):
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

    @property
    def attack(self):
        if self.mutations["FIRE_SPIT"]:
            return "fire"
        elif self.mutations["ELECTRIC_SPIT"]:
            return "electric"
        elif self.mutations["ICE_SPIT"]:
            return "ice"
        else:
            return "acid"

    @property
    def power(self):
        if self.attack == "fire":
            return 4
        elif self.attack == "electric":
            return 3
        elif self.attack == "ice":
            return 2
        else:
            return 1


class Monster(Mob):
    SPEED = 2

    def __init__(self, pos, width, height, life, animation_dict, initial_state):
        super().__init__(pos, width, height, life, animation_dict, initial_state)
        self.prev_state = initial_state
        self.ded: bool = False

        self.last_image: Optional[pygame.surface.Surface] = pygame.surface.Surface((0, 0))

    def idle(self):
        self.prev_state = self.state
        self.animation_dict["idle"] = cycle([next(self.animation_dict[self.state])])
        self.state = "idle"

    def stop_idle(self):
        self.state = self.prev_state

    def move(self, tilemap: tmx.TileMap, dt=1):
        if self.state == "idle" or self.ded: return

        if self.state in {"left", "right"}:
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
        else:
            down = self.state == "down"

            if down:
                self.rect.y += self.SPEED * dt
            else:
                self.rect.y -= self.SPEED * dt

            for tile in tilemap.empty_tiles:
                if tile is None:
                    continue
                if self.rect.colliderect(tile):
                    if down:
                        self.state = "up"
                        self.rect.bottom = tile.top
                    else:
                        self.state = "down"
                        self.rect.top = tile.bottom
                    break


class MobManager(List[Monster]):  # karen style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def good_start(self, player):
        """
        it removes the enemies from the grid if they are too close to the player
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

    def attack(self, enemy: Monster, player: "Player", game: "Game"):
        """
        apply damage to an enemy and if it is too low *KILL*
        """
        duration = 10
        power = player.power

        def init_bul(surf, vel, func):
            enemy.idle()
            game.bullets.append([
                enemy,
                surf,
                pygame.math.Vector2(game.player.rect.center),
                vel,
                game.frame_count + duration,
                list(ATTACKS.keys())[list(ATTACKS.values()).index(surf)],  # quality and dont talk
                func
            ])

        delta = (pygame.math.Vector2(enemy.rect.center) + game.tilemap.offset - pygame.math.Vector2(game.player.rect.center))
        dist = delta.magnitude()

        velocity = delta / dist * duration

        attack = ATTACKS[player.attack]

        if enemy.life <= power:
            init_bul(
                attack,
                velocity,
                lambda: setattr(enemy, "ded", True)
            )
            return

        def m_health():
            self[self.index(enemy)].life -= power

        init_bul(
            attack,
            velocity,
            m_health
        )

    def from_tilemap(self, tilemap: tmx.TileMap, level):
        self.tm = tilemap
        self.clear()
        self.max_life = 3 + level
        for i, row in enumerate(self.tm):
            for j, tile in enumerate(row):
                if tile in tmx.CODE:
                    if is_mob():
                        rep = 7
                        c = random.choice(["left", "right", "up", "down"])
                        p = (j*TL_W + SCIENTIST_SIZE[0], i*TL_H + SCIENTIST_SIZE[1]) if c in "up|down" else (j*TL_W, i*TL_H)
                        self.append(Monster(p, *SCIENTIST_SIZE, self.max_life, {
                                        "right": SpriteSheets.Scientist.WalkRight.get_animation(repeat=rep),
                                        "left": SpriteSheets.Scientist.WalkLeft.get_animation(repeat=rep),
                                        "up": SpriteSheets.Scientist.WalkUp.get_animation(repeat=rep),
                                        "down": SpriteSheets.Scientist.WalkDown.get_animation(repeat=rep)
                                    }, c
                                )
                        )

    def draw(self, surface: pygame.surface.Surface):
        """
        draw
        :param surface:
        :return:
        """
        o = self.tm.offset
        for en in self:
            pp = pygame.Rect(en.rect)
            en.rect.topleft += o
            en.draw(surface)
            en.rect = pp

    def update(self, dt=1):
        """
        moves all of the enemies
        :param dt:
        :return:
        """
        for en in self:
            en.move(self.tm, dt)

    def check_player(self, player: Player) -> Optional[Monster]:
        """
        player-enemy collision check
        :param player:
        :return:
        """
        o = self.tm.offset
        for en in self:
            pp = pygame.Rect(en.rect)
            if player.rect.colliderect((pp.topleft + o, SCIENTIST_SIZE)):
                return en
        return None

    def draw_health(self, surface: pygame.surface.Surface):
        """draw health bar, simple stupid"""
        # i dont want to hear anything for my code
        for en in self:
            if en.ded:
                continue
            r = pygame.Rect(en.rect.topleft + self.tm.offset, (SCIENTIST_SIZE[0], 3))
            r.y -= 5
            pygame.draw.rect(surface, (255, 0, 0), r)
            r.w *= en.life / self.max_life
            pygame.draw.rect(surface, (0, 255, 0), r)
