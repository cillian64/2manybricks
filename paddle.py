import pygame
from math import pi


class Paddle:
    def __init__(self, rect, width, colour):
        """
        rect is a pygame rect describing my position and size.  I'll keep the
        shape and Y-position forever, but am open to updates in x!
        width is the width of the screen, so I know how to not go off teh edges
        colour is a tuple of (red, green, blue)
        """
        self.width = rect.width
        self.height = rect.height
        self.x = rect.left + int(rect.width / 2)
        self.y = rect.top + int(rect.height / 2)
        self.screen_width = width
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect())

    def move(self, pos):
        """
        pos is the result of pygame.mouse.pos, a tuple of (x,y)
        I will ignore the Y coordinate, and take the X coordinate under
        suggestion, so I don't go off the edge of the screen.
        """
        self.x = pos[0]
        if self.x < int(self.width / 2):
            self.x = int(self.width / 2)
        if self.x > self.screen_width - int(self.width / 2):
            self.x = self.screen_width - int(self.width / 2)

    def rect(self):
        return pygame.Rect(self.x - int(self.width / 2),
                           self.y - int(self.height / 2),
                           self.width, self.height)

    def collide(self, ball):
        if (ball.position[0] > self.x - self.width/2 - ball.radius
                and ball.position[0] < self.x + self.width/2 + ball.radius
                and ball.position[1] > self.y - self.height/2 - ball.radius
                and ball.position[1] < self.y + self.height/2):
            siding = (self.x - ball.position[0]) / self.width * 1.25
            ball.bearing = -pi/2 - pi/2 * siding
            ball.position[1] = self.y - int(self.height/2) - ball.radius - 1
            return True
        else:
            return False
