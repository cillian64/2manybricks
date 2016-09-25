import pygame
import os


class Brick:
    def __init__(self, rect, colour, life, multiball=False):
        """
        rect is a pygame rect describing my position and size.
        colour is a tuple of (red, green, blue)
        life is my number of life-points!
        """
        self.multiball = multiball
        self.rect = rect
        self.colour = colour
        if life == 0:
            raise RuntimeError("Cannot have a brick start with life 0")
        self.life = life
        colourcode = "{:02x}{:02x}{:02x}".format(colour[0], colour[1],
                                                 colour[2])
        self.sprites = dict()
        if life == -1:
            self.sprites[-1] = pygame.image.load(
                os.path.join("images", "brick_{}.png".format(colourcode)))
        else:
            for l in range(life, 0, -1):
                self.sprites[l] = pygame.image.load(
                    os.path.join("images", "brick_{}_{}.png".format(
                        colourcode, l)))
        for sprite in self.sprites.values():
            if sprite.get_size() != (rect.width, rect.height):
                raise RuntimeError("Brick is wrong size.  Expected {}"
                                   "".format((rect.width, rect.height)))

    def draw(self, surface):
        surface.blit(self.sprites[self.life], (self.rect.left, self.rect.top))

    def hit(self):
        if self.life > 0:
            self.life -= 1

    def alive(self):
        return (self.life > 0 or self.life == -1)
