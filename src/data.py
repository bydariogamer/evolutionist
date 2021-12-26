# the data that the game will use
from src.spritesheet import SpriteSheet
import src.utils as utils
from pathlib import Path

NAME: str = "Evolutionist"

W: int = 1200
H: int = 700


class PATHS:
    DATA: Path = Path(__file__).parent.parent / "data"
    SPRITESHEETS: Path = Path(__file__).parent.parent / "data" / "spritesheets"


# preload the spritesheets to be less tedious
class SpriteSheets:
    class Elements:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "elements.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "elements.json")

        uranium = sheet.clip(data["uranium"])
        uranium_display = sheet.clip(data["uranium-display"])
        californium = sheet.clip(data["californium"])
        californium_display = sheet.clip(data["californium-display"])
        thorium = sheet.clip(data["thorium"])
        thorium_display = sheet.clip(data["thorium-display"])

    class WireFrame:
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "wireframe.png")
        data = utils.load_json(PATHS.SPRITESHEETS / "wireframe.json")

        # rect like attrs
        topleft = sheet.clip(data["topleft"])
        midtop = sheet.clip(data["midtop"])
        topright = sheet.clip(data["topright"])
        midright = sheet.clip(data["midright"])
        bottomright = sheet.clip(data["bottomright"])
        midbottom = sheet.clip(data["midbottom"])
        midleft = sheet.clip(data["midleft"])
        bottomleft = sheet.clip(data["bottomleft"])
        center = sheet.clip(data["center"])

        # referring to which sides have black outline
        all = sheet.clip(data["all"])
        top = sheet.clip(data["top"])
        bottom = sheet.clip(data["bottom"])
        left = sheet.clip(data["left"])
        right = sheet.clip(data["right"])
        topbottom = sheet.clip(data["topbottom"])
        leftright = sheet.clip(data["leftright"])
