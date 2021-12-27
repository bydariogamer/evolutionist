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

        uranium = sheet.clip(data["uranium"]).convert()
        uranium_display = sheet.clip(data["uranium-display"]).convert()
        californium = sheet.clip(data["californium"]).convert()
        californium_display = sheet.clip(data["californium-display"]).convert()
        thorium = sheet.clip(data["thorium"]).convert()
        thorium_display = sheet.clip(data["thorium-display"]).convert()

    class WireFrame:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "wireframe.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "wireframe.json")

        # rect like attrs
        topleft = sheet.clip(data["topleft"]).convert()
        midtop = sheet.clip(data["midtop"]).convert()
        topright = sheet.clip(data["topright"]).convert()
        midright = sheet.clip(data["midright"]).convert()
        bottomright = sheet.clip(data["bottomright"]).convert()
        midbottom = sheet.clip(data["midbottom"]).convert()
        midleft = sheet.clip(data["midleft"]).convert()
        bottomleft = sheet.clip(data["bottomleft"]).convert()
        center = sheet.clip(data["center"]).convert()

        # referring to which sides have black outline
        all = sheet.clip(data["all"]).convert()
        top = sheet.clip(data["top"]).convert()
        bottom = sheet.clip(data["bottom"]).convert()
        left = sheet.clip(data["left"]).convert()
        right = sheet.clip(data["right"]).convert()
        topbottom = sheet.clip(data["topbottom"]).convert()
        leftright = sheet.clip(data["leftright"]).convert()

        inbottomright = sheet.clip(data["inbottomright"]).convert()
        inbottomleft = sheet.clip(data["inbottomleft"]).convert()
        intopright = sheet.clip(data["intopright"]).convert()
        intopleft = sheet.clip(data["intopleft"]).convert()

        intopbottomright = sheet.clip(data["intopbottomright"]).convert()
        inleftrightbottom = sheet.clip(data["inleftrightbottom"]).convert()
        intopbottomleft = sheet.clip(data["intopbottomleft"]).convert()
        inleftrighttop = sheet.clip(data["inleftrighttop"]).convert()

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
