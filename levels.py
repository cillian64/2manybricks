import pygame
import os

from brick import Brick


class NoMoreLevels(Exception):
    pass


def load_level(level, width, height):
    """
    Load the level number n from the file level_n.png
    The pixels form a 5 row 10 column grid covering 50% of the screen
    leaving the top 20% and the bottom 30% empty
    """
    try:
        im_surf = pygame.image.load(
            os.path.join("levels", "level_{}.png".format(level)))
    except pygame.error:
        raise NoMoreLevels()
    if im_surf.get_size() != (10, 5):
        raise RuntimeError("Level files must be 10 pixels wide by 5 pixels "
                           "high.  This one is {}".format(im_surf.get_size()))
    pixels = pygame.PixelArray(im_surf)
    grid_width = int(width / 10)
    grid_height = int(height / 10)
    bricks = []
    for x in range(10):
        for y in range(5):
            left = x * grid_width
            top = (y + 2) * grid_height
            colour = im_surf.unmap_rgb(pixels[x, y])[:3]  # Strip alpha
            if colour == (0, 0, 0):
                # Black pixel: no brick
                continue
            elif colour == (255, 0, 0):
                # Red pixel: brick with 1 life
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 1))
            elif colour == (255, 255, 0):
                # Yellow pixel: brick with 2 life
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 2))
            elif colour == (0, 255, 0):
                # Green pixel: brick with 3 life
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 3))
            elif colour == (0, 0, 255):
                # Blue pixel: brick with 1 life and multi-ball release!
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height),
                                    colour, 1, multiball=True))
            elif colour == (100, 100, 100):
                # Grey pixel: indestructible brick
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, -1))
            else:
                raise RuntimeError("Invalid colour {} encountered in level {}"
                                   "".format(colour, level))

    return bricks
