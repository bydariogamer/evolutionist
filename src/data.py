# the data that the game will use
from typing import Tuple
from itertools import cycle
from src.spritesheet import SpriteSheet
import src.utils as utils
from pathlib import Path
import pygame


NAME: str = "Evolutionist"

FPS = 60

W: int = 1200
H: int = 700

TILE_SIZE: pygame.math.Vector2 = pygame.math.Vector2(64, 64)
TL_W: int = int(TILE_SIZE[0])
TL_H: int = int(TILE_SIZE[1])

PLAYER_SIZE: Tuple[int, int] = (32, 32)
ELEMENT_SIZE: Tuple[int, int] = (16, 16)
ELEMENT_DISPLAY_SIZE: Tuple[int, int] = (int(40 * 1.5), int(56 * 1.5))
SCIENTIST_SIZE: Tuple[int, int] = (18, 38)
BULLET_SIZE: Tuple[int, int] = (7, 7)

BACKGROUND = pygame.Color(20, 20, 200)


class PATHS:
    DATA: Path = Path(__file__).parent.parent / "data"
    SPRITESHEETS: Path = Path(__file__).parent.parent / "data" / "spritesheets"
    SPRITES: Path = Path(__file__).parent.parent / "data" / "sprites"
    MAPS: Path = Path(__file__).parent.parent / "data" / "maps"
    FONTS: Path = Path(__file__).parent.parent / "data" / "fonts"


class BaseAnimation:  # abstract class
    @classmethod
    def get_animation(cls, repeat: int = 1):
        return cycle(
            [
                getattr(cls, frame)
                for frame in dir(cls)
                for _ in range(repeat)
                if "frame" in frame
            ]
        )


class SingleAnimation:  # abstract class
    """
    when the get_animation method is called it returns a iterable that raises StopIteration when it cant loop anymore
    """
    @classmethod
    def get_animation(cls, repeat: int=1):
        return iter(
            [
                getattr(cls, frame)
                for frame in dir(cls)
                for _ in range(repeat)
                if "frame" in frame
            ]
        )


# preload the spritesheets to be less tedious
class SpriteSheets:
    class Elements:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "elements.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "elements.json")

        uranium = pygame.transform.scale(
            sheet.clip(data["uranium"]).convert_alpha(), ELEMENT_SIZE
        )
        californium = pygame.transform.scale(
            sheet.clip(data["californium"]).convert_alpha(), ELEMENT_SIZE
        )
        thorium = pygame.transform.scale(
            sheet.clip(data["thorium"]).convert_alpha(), ELEMENT_SIZE
        )

        uranium_display = pygame.transform.scale(
            sheet.clip(data["uranium-display"]).convert(), ELEMENT_DISPLAY_SIZE
        )
        californium_display = pygame.transform.scale(
            sheet.clip(data["californium-display"]).convert(), ELEMENT_DISPLAY_SIZE
        )
        thorium_display = pygame.transform.scale(
            sheet.clip(data["thorium-display"]).convert(), ELEMENT_DISPLAY_SIZE
        )

    class WireFrame:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "wireframe.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "wireframe.json")

        # rect like attrs
        topleft = pygame.transform.scale(
            sheet.clip(data["topleft"]), TILE_SIZE
        ).convert()
        midtop = pygame.transform.scale(sheet.clip(data["midtop"]), TILE_SIZE).convert()
        topright = pygame.transform.scale(
            sheet.clip(data["topright"]), TILE_SIZE
        ).convert()
        midright = pygame.transform.scale(
            sheet.clip(data["midright"]), TILE_SIZE
        ).convert()
        bottomright = pygame.transform.scale(
            sheet.clip(data["bottomright"]), TILE_SIZE
        ).convert()
        midbottom = pygame.transform.scale(
            sheet.clip(data["midbottom"]), TILE_SIZE
        ).convert()
        midleft = pygame.transform.scale(
            sheet.clip(data["midleft"]), TILE_SIZE
        ).convert()
        bottomleft = pygame.transform.scale(
            sheet.clip(data["bottomleft"]), TILE_SIZE
        ).convert()
        center = pygame.transform.scale(sheet.clip(data["center"]), TILE_SIZE).convert()

        # referring to which sides have black outline
        all = pygame.transform.scale(sheet.clip(data["all"]), TILE_SIZE).convert()
        top = pygame.transform.scale(sheet.clip(data["top"]), TILE_SIZE).convert()
        bottom = pygame.transform.scale(sheet.clip(data["bottom"]), TILE_SIZE).convert()
        left = pygame.transform.scale(sheet.clip(data["left"]), TILE_SIZE).convert()
        right = pygame.transform.scale(sheet.clip(data["right"]), TILE_SIZE).convert()
        topbottom = pygame.transform.scale(
            sheet.clip(data["topbottom"]), TILE_SIZE
        ).convert()
        leftright = pygame.transform.scale(
            sheet.clip(data["leftright"]), TILE_SIZE
        ).convert()

        inbottomright = pygame.transform.scale(
            sheet.clip(data["inbottomright"]), TILE_SIZE
        ).convert()
        inbottomleft = pygame.transform.scale(
            sheet.clip(data["inbottomleft"]), TILE_SIZE
        ).convert()
        intopright = pygame.transform.scale(
            sheet.clip(data["intopright"]), TILE_SIZE
        ).convert()
        intopleft = pygame.transform.scale(
            sheet.clip(data["intopleft"]), TILE_SIZE
        ).convert()

        intopbottomright = pygame.transform.scale(
            sheet.clip(data["intopbottomright"]), TILE_SIZE
        ).convert()
        inleftrightbottom = pygame.transform.scale(
            sheet.clip(data["inleftrightbottom"]), TILE_SIZE
        ).convert()
        intopbottomleft = pygame.transform.scale(
            sheet.clip(data["intopbottomleft"]), TILE_SIZE
        ).convert()
        inleftrighttop = pygame.transform.scale(
            sheet.clip(data["inleftrighttop"]), TILE_SIZE
        ).convert()

    class GreenSlime:
        class WalkRight(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-right.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), PLAYER_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), PLAYER_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), PLAYER_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), PLAYER_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), PLAYER_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), PLAYER_SIZE
            ).convert_alpha()
            frame7 = pygame.transform.scale(
                sheet.clip(data["frames"]["7"]), PLAYER_SIZE
            ).convert_alpha()
            frame8 = pygame.transform.scale(
                sheet.clip(data["frames"]["8"]), PLAYER_SIZE
            ).convert_alpha()

            animation = cycle(
                [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8]
            )

        class WalkLeft(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-right.json")

            frame1 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["1"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["2"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["3"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["4"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["5"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["6"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame7 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["7"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()
            frame8 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["8"]), True, False),
                PLAYER_SIZE,
            ).convert_alpha()

            animation = cycle(
                [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8]
            )

        class WalkUp(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-up.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-up.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), PLAYER_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), PLAYER_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), PLAYER_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), PLAYER_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), PLAYER_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), PLAYER_SIZE
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

        class Idle(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-idle.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "slime-green-idle.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), PLAYER_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), PLAYER_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), PLAYER_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), PLAYER_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), PLAYER_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), PLAYER_SIZE
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

    class Scientist:
        class WalkRight(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-right.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame7 = pygame.transform.scale(
                sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7])

        class WalkLeft(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-right.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-right.json")

            frame1 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["1"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["2"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["3"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["4"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["5"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["6"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()
            frame7 = pygame.transform.scale(
                pygame.transform.flip(sheet.clip(data["frames"]["7"]), True, False),
                SCIENTIST_SIZE,
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6, frame7])

        class WalkUp(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-up.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-up.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

        class WalkDown(BaseAnimation):
            sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-running-down.png")
            data = utils.load_json(PATHS.SPRITESHEETS / "scientist-running-down.json")

            frame1 = pygame.transform.scale(
                sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame2 = pygame.transform.scale(
                sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame3 = pygame.transform.scale(
                sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame4 = pygame.transform.scale(
                sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame5 = pygame.transform.scale(
                sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE
            ).convert_alpha()
            frame6 = pygame.transform.scale(
                sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE
            ).convert_alpha()

            animation = cycle([frame1, frame2, frame3, frame4, frame5, frame6])

        # this took longer to get back to this stage because black had touched this code :joy:
        class DeathAnimations:
            class ElectrifiedRight(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-electrified-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-electrified-right.json")

                frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha()
                frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha()
                frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha()
                frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha()
                frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha()
                frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha()
                frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha()
                frame8 = pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha()

            class ElectrifiedLeft(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-electrified-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-electrified-right.json")

                frame1 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame2 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame3 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame4 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame5 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame6 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame7 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame8 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha(), True, False)

            class FreezingRight(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-freezing-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-freezing-right.json")

                frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha()
                frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha()
                frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha()
                frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha()
                frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha()
                frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha()
                frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha()
                frame8 = pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha()

            class FreezingLeft(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-freezing-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-freezing-right.json")

                frame1 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame2 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame3 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame4 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame5 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame6 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame7 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame8 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha(), True, False)

            class OnFireRight(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-onfire-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-onfire-right.json")

                frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha()
                frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha()
                frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha()
                frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha()
                frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha()
                frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha()
                frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha()
                frame8 = pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha()

            class OnFireLeft(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-onfire-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-onfire-right.json")

                frame1 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame2 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame3 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame4 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame5 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame6 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame7 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame8 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha(), True, False)

            class AcidRight(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-disolved-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-disolved-right.json")

                frame1 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame2 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame3 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame4 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame5 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame6 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame7 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha(), True, False)
                frame8 = pygame.transform.flip(pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha(), True, False)

            class AcidLeft(SingleAnimation):
                sheet = SpriteSheet(PATHS.SPRITESHEETS / "scientist-disolved-right.png")
                data = utils.load_json(PATHS.SPRITESHEETS / "scientist-disolved-right.json")

                frame1 = pygame.transform.scale(sheet.clip(data["frames"]["1"]), SCIENTIST_SIZE).convert_alpha()
                frame2 = pygame.transform.scale(sheet.clip(data["frames"]["2"]), SCIENTIST_SIZE).convert_alpha()
                frame3 = pygame.transform.scale(sheet.clip(data["frames"]["3"]), SCIENTIST_SIZE).convert_alpha()
                frame4 = pygame.transform.scale(sheet.clip(data["frames"]["4"]), SCIENTIST_SIZE).convert_alpha()
                frame5 = pygame.transform.scale(sheet.clip(data["frames"]["5"]), SCIENTIST_SIZE).convert_alpha()
                frame6 = pygame.transform.scale(sheet.clip(data["frames"]["6"]), SCIENTIST_SIZE).convert_alpha()
                frame7 = pygame.transform.scale(sheet.clip(data["frames"]["7"]), SCIENTIST_SIZE).convert_alpha()
                frame8 = pygame.transform.scale(sheet.clip(data["frames"]["8"]), SCIENTIST_SIZE).convert_alpha()

    class Bullets:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "bullets.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "bullets.json")

        electro = pygame.transform.scale(sheet.clip(data["electro"]), BULLET_SIZE)
        ice = pygame.transform.scale(sheet.clip(data["ice"]), BULLET_SIZE)
        fire = pygame.transform.scale(sheet.clip(data["fire"]), BULLET_SIZE)
        acid = pygame.transform.scale(sheet.clip(data["acid"]), BULLET_SIZE)


class Images:
    DNA = pygame.image.load(PATHS.SPRITES / "DNA.png").convert_alpha()
    TABLE = pygame.image.load(PATHS.SPRITES / "table.png").convert_alpha()


class Fonts:
    pixel_font = pygame.font.Font(PATHS.FONTS / "pixelFont.ttf", 20)
