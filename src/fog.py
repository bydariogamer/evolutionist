from typing import *
import src.tilemap as tm
from src.utils import *
from src.data import *
import pygame


CODE = tm.CODE


SURFACES = {
    255: pygame.surface.Surface(TILE_SIZE),
    191: pygame.surface.Surface(TILE_SIZE),
    127: pygame.surface.Surface(TILE_SIZE),
    63 : pygame.surface.Surface(TILE_SIZE),
    0  : pygame.surface.Surface(TILE_SIZE),
}

for v in SURFACES:
    SURFACES[v].set_alpha(v)


class Fog(List[List[int]]):

    def from_tilemap(self, tilemap: tm.TileMap):
        self.tm = tilemap
        self.clear()
        for row in self.tm:
            self.append(len(row)*[255])

    @property
    def offset(self):
        return self.tm.offset

    def update(self, player):
        j, i = (round(x) for x in (pygame.math.Vector2(player.rect.center) - self.offset).elementwise() // TILE_SIZE)
        self[i][j] = 0
        for [i, j] in [
            (i, j - 1),
            (i + 1, j),
            (i, j + 1),
            (i - 1, j),
            (i + 1, j + 1),
            (i + 1, j - 1),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 2, j),
            (i - 2, j),
            (i, j + 2),
            (i, j - 2)
        ]:
            if i in range(len(self)) and j in range(len(self[i])):
                self[i][j] = 0

    def draw(self, surface: pygame.surface.Surface):
        x, y = self.offset
        r = surface.get_rect()

        surface.blits(
            (
                (
                    SURFACES[tile],
                    [j*TL_W + x, i*TL_H + y]
                 ) for i, row in enumerate(self) for j, tile in enumerate(row)
                if tile and r.colliderect([j*TL_W + x, i*TL_H + y, *TILE_SIZE])
        )
            , False
        )
