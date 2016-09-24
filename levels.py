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
    pixels = pygame.PixelArray(im_surf)
    if pixels.shape != (10, 5):
        raise RuntimeError("Level files must be 10 pixels wide by 5 pixels "
                           "high.  This one is {}".format(pixels.shape))
    grid_width = int(width / 10)
    grid_height = int(height / 10)
    bricks = []
    for x in range(10):
        for y in range(5):
            left = x * grid_width
            top = (y + 2) * grid_height
            colour = im_surf.unmap_rgb(pixels[x, y])[:3]  # Strip alpha
            if colour == (0, 0, 0):
                continue
            elif colour == (255, 0, 0):
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 1))
            elif colour == (255, 255, 0):
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 2))
            elif colour == (0, 255, 0):
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, 3))
            elif colour == (100, 100, 100):
                bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                                grid_height), colour, -1))
            else:
                raise RuntimeError("Invalid colour {} encountered in level {}"
                                   "".format(colour, level))

    return bricks
