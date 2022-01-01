import pygame
from typing import List

import src.tilemap as tm
from src.data import *
from src.utils import *


CODE = tm.CODE

SURFACES = {
    255: pygame.surface.Surface(TILE_SIZE),
    191: pygame.surface.Surface(TILE_SIZE),
    127: pygame.surface.Surface(TILE_SIZE),
    63: pygame.surface.Surface(TILE_SIZE),
    0: pygame.surface.Surface(TILE_SIZE),
}

for v in SURFACES:
    SURFACES[v].set_alpha(v)


class Fog(List[List[int]]):
    def from_tilemap(self, tilemap: tm.TileMap):
        self.tilemap = tilemap
        self.clear()
        for row in self.tilemap:
            self.append(len(row) * [255])

    @property
    def offset(self):
        return self.tilemap.offset

    def update(self, player):
        x, y = (
            round(coord)
            for coord in (
                pygame.math.Vector2(player.rect.center) - self.offset
            ).elementwise()
            // TILE_SIZE
        )
        for i in range(-3, 4):
            for j in range(-3, 4):
                if x + i in range(len(self[i])) and y + j in range(len(self)):
                    self[y + j][x + i] = 191
        for i in range(-2, 3):
            for j in range(-2, 3):
                if x + i in range(len(self[i])) and y + j in range(len(self)):
                    self[y + j][x + i] = 63
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if x + i in range(len(self[i])) and y + j in range(len(self)):
                    self[y + j][x + i] = 0

    def draw(self, surface: pygame.surface.Surface):
        x, y = self.offset
        r = surface.get_rect()
        surface.blits(
            [
                (SURFACES[tile], [j * TL_W + x, i * TL_H + y])
                for i, row in enumerate(self)
                for j, tile in enumerate(row)
                if tile and r.colliderect([j * TL_W + x, i * TL_H + y, *TILE_SIZE])
            ],
            False,
        )
