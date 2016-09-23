import pygame


class Brick:
    def __init__(self, rect, colour, life):
        """
        rect is a pygame rect describing my position and size.
        colour is a tuple of (red, green, blue)
        life is my number of life-points!
        """
        self.rect = rect
        self.colour = colour
        self.life = life

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def hit(self):
        if self.life > 0:
            self.life -= 1

    def alive(self):
        return (self.life > 0 or self.life == -1)
