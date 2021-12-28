# the data that the game will use
from typing import Tuple
from itertools import cycle
from src.spritesheet import SpriteSheet
import src.utils as utils
from pathlib import Path
import pygame


NAME: str = "Evolutionist"

W: int = 1200
H: int = 700

TILE_SIZE: pygame.math.Vector2 = pygame.math.Vector2(64, 64)
TL_W: int = int(TILE_SIZE[0])
TL_H: int = int(TILE_SIZE[1])

PLAYER_SIZE: Tuple[int, int] = (32, 32)
ELEMENT_SIZE: Tuple[int, int] = (16, 16)
ELEMENT_DISPLAY_SIZE: Tuple[int, int] = (int(40 * 1.5), int(56 * 1.5))


class PATHS:
    DATA: Path = Path(__file__).parent.parent / "data"
    SPRITESHEETS: Path = Path(__file__).parent.parent / "data" / "spritesheets"
    MAPS: Path = Path(__file__).parent.parent / "data" / "maps"


class BaseAnimation:  # abstract class
    @classmethod
    def get_animation(cls, repeat: int=1):
        return cycle([
            getattr(cls, frame) for frame in dir(cls) for _ in range(repeat) if "frame" in frame
        ])


# preload the spritesheets to be less tedious
class SpriteSheets:
    class Elements:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "elements.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "elements.json")

        uranium = pygame.transform.scale(sheet.clip(data["uranium"]).convert_alpha(), ELEMENT_SIZE)
        californium = pygame.transform.scale(sheet.clip(data["californium"]).convert_alpha(), ELEMENT_SIZE)
        thorium = pygame.transform.scale(sheet.clip(data["thorium"]).convert_alpha(), ELEMENT_SIZE)

        uranium_display = pygame.transform.scale(sheet.clip(data["uranium-display"]).convert(), ELEMENT_DISPLAY_SIZE)
        californium_display = pygame.transform.scale(sheet.clip(data["californium-display"]).convert(), ELEMENT_DISPLAY_SIZE)
        thorium_display = pygame.transform.scale(sheet.clip(data["thorium-display"]).convert(), ELEMENT_DISPLAY_SIZE)

    class WireFrame:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "wireframe.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "wireframe.json")

        # rect like attrs
        topleft = pygame.transform.scale(sheet.clip(data["topleft"]), TILE_SIZE).convert()
        midtop = pygame.transform.scale(sheet.clip(data["midtop"]), TILE_SIZE).convert()
        topright = pygame.transform.scale(sheet.clip(data["topright"]), TILE_SIZE).convert()
        midright = pygame.transform.scale(sheet.clip(data["midright"]), TILE_SIZE).convert()
        bottomright = pygame.transform.scale(sheet.clip(data["bottomright"]), TILE_SIZE).convert()
        midbottom = pygame.transform.scale(sheet.clip(data["midbottom"]), TILE_SIZE).convert()
        midleft = pygame.transform.scale(sheet.clip(data["midleft"]), TILE_SIZE).convert()
        bottomleft = pygame.transform.scale(sheet.clip(data["bottomleft"]), TILE_SIZE).convert()
        center = pygame.transform.scale(sheet.clip(data["center"]), TILE_SIZE).convert()

        # referring to which sides have black outline
        all = pygame.transform.scale(sheet.clip(data["all"]), TILE_SIZE).convert()
        top = pygame.transform.scale(sheet.clip(data["top"]), TILE_SIZE).convert()
        bottom = pygame.transform.scale(sheet.clip(data["bottom"]), TILE_SIZE).convert()
        left = pygame.transform.scale(sheet.clip(data["left"]), TILE_SIZE).convert()
        right = pygame.transform.scale(sheet.clip(data["right"]), TILE_SIZE).convert()
        topbottom = pygame.transform.scale(sheet.clip(data["topbottom"]), TILE_SIZE).convert()
        leftright = pygame.transform.scale(sheet.clip(data["leftright"]), TILE_SIZE).convert()

        inbottomright = pygame.transform.scale(sheet.clip(data["inbottomright"]), TILE_SIZE).convert()
        inbottomleft = pygame.transform.scale(sheet.clip(data["inbottomleft"]), TILE_SIZE).convert()
        intopright = pygame.transform.scale(sheet.clip(data["intopright"]), TILE_SIZE).convert()
        intopleft = pygame.transform.scale(sheet.clip(data["intopleft"]), TILE_SIZE).convert()

        intopbottomright = pygame.transform.scale(sheet.clip(data["intopbottomright"]), TILE_SIZE).convert()
        inleftrightbottom = pygame.transform.scale(sheet.clip(data["inleftrightbottom"]), TILE_SIZE).convert()
        intopbottomleft = pygame.transform.scale(sheet.clip(data["intopbottomleft"]), TILE_SIZE).convert()
        inleftrighttop = pygame.transform.scale(sheet.clip(data["inleftrighttop"]), TILE_SIZE).convert()

    class GreenSlime:
        class WalkRight(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-right.json")

            frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), PLAYER_SIZE).convert_alpha()
            frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), PLAYER_SIZE).convert_alpha()
            frame8 = pygame.transform.scale(sheet.clip(data["frames"]["8"]), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8])

        class WalkLeft(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-right.json")

            frame1 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["1"]), True, False), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["2"]), True, False), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["3"]), True, False), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["4"]), True, False), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["5"]), True, False), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["6"]), True, False), PLAYER_SIZE).convert_alpha()
            frame7 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["7"]), True, False), PLAYER_SIZE).convert_alpha()
            frame8 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["8"]), True, False), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8])

        class WalkUp(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-up.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-up.json")

            frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

        class Idle(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-idle.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-idle.json")

            frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

    class Scientist:
        class WalkRight(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-right.json")

            frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), PLAYER_SIZE).convert_alpha()
            frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7])

        class WalkLeft(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-right.json")

            frame1 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["1"]), True, False), PLAYER_SIZE).convert_alpha()
            frame2 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["2"]), True, False), PLAYER_SIZE).convert_alpha()
            frame3 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["3"]), True, False), PLAYER_SIZE).convert_alpha()
            frame4 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["4"]), True, False), PLAYER_SIZE).convert_alpha()
            frame5 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["5"]), True, False), PLAYER_SIZE).convert_alpha()
            frame6 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["6"]), True, False), PLAYER_SIZE).convert_alpha()
            frame7 = pygame.transform.scale(pygame.transform.flip(sheet.clip(data["frames"]["7"]), True, False), PLAYER_SIZE).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7])
