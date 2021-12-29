from typing import *
import pygame
import json
import math
import sys
import functools


# colors have also alpha
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
BLUE = (30, 144, 255, 255)
TRUE_BLUE = (0, 0, 255, 255)
PURPLE = (155, 89, 182, 255)
RED = (255, 0, 0, 255)
GREEN = (60, 179, 113, 255)
DK_GREEN = (46, 139, 87, 255)
ORANGE = (230, 140, 30, 255)
GREY = (128, 128, 128, 255)
LIGHT_GREY = (192, 192, 192, 255)
PINK = (255, 51, 153, 255)
FLASH_GREEN = (153, 255, 0, 255)
NAVY = (0, 0, 128, 255)
GOLD = (255, 214, 0, 255)
WHITESMOKE = (245, 245, 245, 255)

# from https://flatuicolors.com/ :D
TURQUOISE = (26, 188, 156, 255)
YELLOW = (241, 196, 15, 255)
CONCRETE = (149, 165, 166, 255)
PUMPKIN = (211, 84, 0, 255)
NICE_BLUE = (52, 152, 219, 255)
MIDNIGHT_BLUE = (44, 62, 80, 255)

# some alignments that are used
CENTER = "center"
TOPLEFT = "topleft"
BOTTOMLEFT = "bottomleft"
TOPRIGHT = "topright"
BOTTOMRIGHT = "bottomright"
MIDTOP = "midtop"
MIDLEFT = "midleft"
MIDBOTTOM = "midbottom"
MIDRIGHT = "midright"


@functools.lru_cache
def load_image(path: str) -> pygame.surface.Surface:
    return pygame.image.load(path).convert()


@functools.lru_cache
def load_alpha_image(path: str) -> pygame.surface.Surface:
    return pygame.image.load(path).convert_alpha()


@functools.lru_cache
def resize_smooth_image(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    return pygame.transform.smoothscale(image, new_size)


@functools.lru_cache
def resize_image(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    return pygame.transform.scale(image, new_size)


@functools.lru_cache
def resize_image_ratio(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    ratio = new_size[0] / image.get_width()
    return pygame.transform.scale(
        image,
        (math.floor(image.get_width() * ratio), math.floor(image.get_height() * ratio)),
    )


@functools.lru_cache
def resizex(
    image: pygame.surface.Surface, amount: int or float
) -> pygame.surface.Surface:
    w, h = image.get_width(), image.get_height()
    return pygame.transform.scale(image, (w * amount, h * amount))


def left_click(event: pygame.event.Event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False


def middle_click(event: pygame.event.Event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2:
            return True
    return False


def right_click(event: pygame.event.Event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False


@functools.lru_cache
def get_font(size, type_of_font="comicsans") -> pygame.font.Font:
    if type_of_font.endswith(".tff"):
        font = pygame.font.Font(type_of_font, size)
        return font

    font = pygame.font.SysFont(type_of_font, size)
    return font


def wrap_multi_lines(
    text: str,
    font: pygame.font.Font,
    max_width: int,
    max_height: int = 0,
    antialias: bool = True,
) -> List:
    finished_lines = [""]

    for word in text.split(" "):
        w = font.render(word, antialias, BLACK).get_width()
        # check if one word is too long to fit in one line
        if w > max_width:
            sys.exit(
                f"""the word: "{word}" is too long to fit in a width of: {max_width}, out of bounds by: {w - max_width}pxls"""
            )

        if (
            font.render(finished_lines[-1] + word, antialias, BLACK).get_width()
            > max_width
        ):
            finished_lines.append(f"""{word}""")
        else:
            finished_lines[-1] += f""" {word}"""
    finished_lines[0] = finished_lines[0][1:]
    if max_height > 0:
        h = 0
        for line in finished_lines:
            h += font.render(line, antialias, BLACK).get_height()

        if h > max_height:
            sys.exit(
                f"""the lines: {finished_lines} are too long in the y axis by: {h - max_height}pxls"""
            )

    return finished_lines


def blit_multiple_lines(
    x: int,
    y: int,
    lines: list,
    WIN: pygame.surface.Surface,
    font: pygame.font.Font,
    centered_x=False,
    centered_x_pos: int = None,
    color: Tuple[int, int, int] = (0, 0, 0),
) -> None:
    if centered_x and not centered_x_pos:
        sys.exit("Missing 'centered_x_pos'")
    height = font.get_height()
    for i, text in enumerate(lines):
        rendered_text_surface = font.render(text, True, color)

        if centered_x:
            WIN.blit(
                rendered_text_surface,
                (
                    centered_x_pos - rendered_text_surface.get_width() / 2,
                    y + (i * height),
                ),
            )

        else:
            WIN.blit(rendered_text_surface, (x, y + (i * height)))


def pixel_perfect_collision(
    image_1: pygame.surface.Surface,
    image_1_pos: Tuple[int, int],
    image_2: pygame.surface.Surface,
    image_2_pos: Tuple[int, int],
) -> bool:
    offset = [image_1_pos[0] - image_2_pos[0], image_1_pos[1] - image_2_pos[1]]
    mask_1 = pygame.mask.from_surface(image_1)
    mask_2 = pygame.mask.from_surface(image_2)

    result = mask_2.overlap(mask_1, offset)
    if result:
        return True
    return False


def load_json(path):
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data


def flatten(items):
    for item in items:
        if isinstance(item, list) or isinstance(item, tuple):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item
