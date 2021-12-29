from typing import *
import src.tilemap as tmx
from src.utils import *
from src.data import *
import random
import pygame


CHANCE_FOR_ELEMENT = 0.95  # 5% of tiles will have elements
ELEMENT_PER_CHANCE = 0.6  # if it is smaller than that then it is uranium then the gen goes again and falls into thorium then falls into californium

rand = random.random

# PEP8 shut up, this clean def not
is_el = lambda: rand() > CHANCE_FOR_ELEMENT
what_el = (
    lambda: 1
    if rand() < ELEMENT_PER_CHANCE
    else 5
    if rand() < ELEMENT_PER_CHANCE
    else 3
)


CODE = {
    1: SpriteSheets.Elements.uranium,
    2: SpriteSheets.Elements.uranium_display,
    3: SpriteSheets.Elements.californium,
    4: SpriteSheets.Elements.californium_display,
    5: SpriteSheets.Elements.thorium,
    6: SpriteSheets.Elements.thorium_display,
}

font = pygame.font.Font(PATHS.DATA / "fonts" / "pixelFont.ttf", 20)


class Elements(List[List[int]]):
    def from_tilemap(self, tilemap: tmx.TileMap):
        self.tm = tilemap
        self.clear()
        for row in self.tm:
            self.append([])
            for tile in row:
                if tile in tmx.CODE:
                    if is_el():
                        self[~0].append(what_el())
                    else:
                        self[~0].append(-1)
                else:
                    self[~0].append(-1)
        self.uranium_count: int = 0
        self.californium_count: int = 0
        self.thorium_count: int = 0

    @property
    def offset(self):
        return self.tm.offset

    def update(self, player):
        # dont talk about it
        r = pygame.Rect(player.rect)  # copy cause retarded
        r.x -= self.offset.x
        r.y -= self.offset.y

        for i, row in enumerate(self):
            for j, item in enumerate(row):
                if item not in CODE:
                    continue
                if r.colliderect(
                    [
                        j * TL_W + ELEMENT_SIZE[0] / 2,
                        i * TL_H + ELEMENT_SIZE[1] / 2,
                        *ELEMENT_SIZE,
                    ]
                ):
                    v = self[i][j]
                    if v == 1:
                        self.uranium_count += 1
                    elif v == 3:
                        self.californium_count += 1
                    elif v == 5:
                        self.thorium_count += 1
                    self[i][j] = -1

    def draw_elements(self, surface: pygame.surface.Surface):
        x, y = self.offset
        r = surface.get_rect()

        surface.blits(
            [
                (
                    CODE[tile],
                    [
                        j * TL_W + x + ELEMENT_SIZE[0] * 2 / 1.5,
                        i * TL_H + y + ELEMENT_SIZE[1] * 2 / 1.5,
                    ],
                )
                for i, row in enumerate(self)
                for j, tile in enumerate(row)
                if tile in CODE
                and r.colliderect(
                    [
                        j * TL_W + x + ELEMENT_SIZE[0] * 2 / 1.5,
                        i * TL_H + y + ELEMENT_SIZE[1] * 2 / 1.5,
                        *TILE_SIZE,
                    ]
                )
            ],
            False,
        )

    def draw_labels(self, surface: pygame.surface.Surface):
        # dont say a word about my **awesome** code
        x = [0]
        for i in (2, 4):
            x.append(CODE[i].get_width())
        x[2] += x[1]
        surface.blits(
            (
                (CODE[[2, 4, 6][i]], [x[i], H - CODE[[2, 4, 6][i]].get_height()])
                for i in range(3)
            ),
            False,
        )
        clr = (50, 50, 50)
        surface.blit(
            font.render(str(self.uranium_count), True, clr),
            (30, H - font.render(str(self.uranium_count), True, clr).get_height() - 7 + 5),
        )
        surface.blit(
            font.render(str(self.californium_count), True, clr),
            (95, H - font.render(str(self.californium_count), True, clr).get_height() - 7 + 5),
        )
        surface.blit(
            font.render(str(self.thorium_count), True, clr),
            (160, H - font.render(str(self.thorium_count), True, clr).get_height() - 7 + 5),
        )
