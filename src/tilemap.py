from csv import reader as CSVReader
from src.utils import *
from src.data import *
import pygame


CODE: Dict[int, pygame.surface.Surface] = {
    0: SpriteSheets.WireFrame.topleft,
    1: SpriteSheets.WireFrame.midtop,
    2: SpriteSheets.WireFrame.topright,
    3: SpriteSheets.WireFrame.top,
    4: SpriteSheets.WireFrame.inbottomright,
    5: SpriteSheets.WireFrame.inbottomleft,
    6: SpriteSheets.WireFrame.midleft,
    7: SpriteSheets.WireFrame.center,
    8: SpriteSheets.WireFrame.midright,
    9: SpriteSheets.WireFrame.leftright,
    10: SpriteSheets.WireFrame.intopright,
    11: SpriteSheets.WireFrame.intopleft,
    12: SpriteSheets.WireFrame.bottomleft,
    13: SpriteSheets.WireFrame.midbottom,
    14: SpriteSheets.WireFrame.bottomright,
    15: SpriteSheets.WireFrame.bottom,
    16: SpriteSheets.WireFrame.intopbottomright,
    17: SpriteSheets.WireFrame.inleftrightbottom,
    18: SpriteSheets.WireFrame.left,
    19: SpriteSheets.WireFrame.topbottom,
    20: SpriteSheets.WireFrame.right,
    21: SpriteSheets.WireFrame.all,
    22: SpriteSheets.WireFrame.intopbottomleft,
    23: SpriteSheets.WireFrame.inleftrighttop,
}


class TileMap(List[List[int]]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.empty_tiles: List[pygame.Rect] = []

    def load(self, path):
        self.offset *= 0
        with open(path, "r") as f:
            self.clear()
            self.empty_tiles.clear()
            for i, ln in enumerate(CSVReader(f)):
                self.append([])
                for j, l in enumerate(ln):
                    l = int(l)
                    if l not in CODE:
                        l = None
                        self.empty_tiles.append(pygame.Rect(j * TL_W, i * TL_H, *TILE_SIZE))  # x, y
                    self[~0].append(l)

    def draw(self, surface: pygame.surface.Surface) -> None:
        x, y = self.offset
        r = surface.get_rect()
        surface.blits(
            (
                (CODE[tile], [j * TL_W + x, i * TL_H + y])
                for i, row in enumerate(self)
                for j, tile in enumerate(row)
                if tile is not None
                and r.colliderect([j * TL_W + x, i * TL_H + y, *TILE_SIZE])
            ),
            False,
        )
