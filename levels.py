import pygame

from brick import Brick


def load_level(n, width, height):
    """
    Load the level number n from the file level_n.png
    The pixels form a 5 row 10 column grid covering 50% of the screen
    leaving the top 20% and the bottom 30% empty
    """
    im_surf = pygame.image.load("level_{}.png".format(n))
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
            colour = im_surf.unmap_rgb(pixels[x, y])
            bricks.append(Brick(pygame.Rect(left, top, grid_width,
                                            grid_height), colour, 1))
    return bricks
