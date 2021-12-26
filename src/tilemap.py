from csv import reader
from src.utils import *
from src.data import *
import pygame


class BaseTile:  # inheritance reasons
    __slots__ = "rect", "sprite"

    def __init__(self, x: int, y: int):
        self.rect: pygame.Rect = pygame.Rect((x, y), (10, 10))
        self.sprite: pygame.surface.Surface  # undefined


class CollideTile(BaseTile): ...  # to be able to decide if we are going to check for a collision


# define it here so we can just reference the images instead of having to load so many images
class Tiles:
    class WireFrame:
        class topleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.topleft

        class midtop(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.midtop

        class topright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.topright

        class midright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.midright

        class bottomright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.bottomright

        class midbottom(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.midbottom

        class midleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.midleft

        class bottomleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.bottomleft

        class center(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.center

        class all(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.all

        class top(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.top

        class bottom(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.bottom

        class left(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.left

        class right(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.right

        class topbottom(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.topbottom

        class leftright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.leftright

        class inbottomright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.inbottomright

        class inbottomleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.inbottomleft

        class intopright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.intopright

        class intopleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.intopleft

        class intopbottomright(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.intopbottomright

        class inleftrightbottom(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.inleftrightbottom

        class intopbottomleft(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.intopbottomleft

        class inleftrighttop(BaseTile):
            def __init__(self, x: int, y: int):
                super().__init__(x, y)
                self.sprite = SpriteSheets.WireFrame.inleftrighttop


CODE: Dict[int, BaseTile] = {
    0 : Tiles.WireFrame.topleft,
    1 : Tiles.WireFrame.midtop,
    2 : Tiles.WireFrame.topright,
    3 : Tiles.WireFrame.top,
    4 : Tiles.WireFrame.inbottomright,
    5 : Tiles.WireFrame.inbottomleft,
    6 : Tiles.WireFrame.midleft,
    7 : Tiles.WireFrame.center,
    8 : Tiles.WireFrame.midright,
    9 : Tiles.WireFrame.leftright,
    10: Tiles.WireFrame.intopright,
    11: Tiles.WireFrame.intopleft,
    12: Tiles.WireFrame.bottomleft,
    13: Tiles.WireFrame.midbottom,
    14: Tiles.WireFrame.bottomright,
    15: Tiles.WireFrame.bottom,
    16: Tiles.WireFrame.intopbottomright,
    17: Tiles.WireFrame.inleftrightbottom,
    18: Tiles.WireFrame.left,
    19: Tiles.WireFrame.topbottom,
    20: Tiles.WireFrame.right,
    21: Tiles.WireFrame.all,
    22: Tiles.WireFrame.intopbottomleft,
    23: Tiles.WireFrame.inleftrighttop,
}


class TileMap:
    def __init__(self):
        self.grid: Set[BaseTile] = set()

    def load(self, path):
        with open(path, "r") as f:
            for i, ln in enumerate(reader(f)):
                for j, l in enumerate(ln):
                    l = int(l)
                    if l not in CODE: continue
                    self.grid.add(
                        CODE[l](j * TL_W, i * TL_H)
                    )
            for tile in self.grid:
                tile.sprite = pygame.transform.scale(tile.sprite, TILE_SIZE)

    def draw(self, surface: pygame.surface.Surface) -> None:
        surface.blits(
            [(tile.sprite, tile.rect) for tile in self.grid], False
        )
