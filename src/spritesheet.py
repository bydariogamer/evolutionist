from typing import Union, List, Tuple
import pygame


class SpriteSheet:
    """
    my_sheet = SpriteSheet(path_to_image)

    image = my_sheet.clip([0, 0, 12, 12])  # returns a new surface with the data from the given area
    """
    def __init__(self, path: str, colorkey: Union[Tuple[int, int, int], List[int], int]=None):
        self.sheet: pygame.surface.Surface = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            if colorkey == -1:
                self.sheet.set_colorkey(self.sheet.get_at((0, 0)), pygame.RLEACCEL)
            else:
                self.sheet.set_colorkey(colorkey, pygame.RLEACCEL)

    def get_sheet(self) -> pygame.surface.Surface:
        return self.sheet

    def clip(self, r, colorkey=None) -> pygame.surface.Surface:
        image = self.sheet.subsurface(pygame.Rect(r))
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def clips(self, rects, colorkey=None) -> List[pygame.surface.Surface]:
        return [self.clip(r, colorkey) for r in rects]
