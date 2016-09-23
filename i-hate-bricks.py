import sys
import pygame
from math import sin, cos, pi

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
ball_defaults = {'position': [int(width/2), int(height/2)],
                 'bearing': -1.3,
                 'speed': 5,
                 'radius': 10,
                 'colour': (255, 0, 0)
                 }
background = (0, 0, 0)


class Ball:
    def __init__(self, position, bearing, speed, radius, colour):
        """
        Position is a *LIST* of [x, y] in pixels.  So I can mutate them.
        Bearing is in radians anticlockwise from right ->
        Speed is in pixels per tick
        Radius is in pixels
        Colour is a tuple of (red, green, blue) integers 0-255
        """
        self.position = position
        self.bearing = bearing
        self.speed = speed
        self.radius = radius
        self.colour = colour

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.position, self.radius)

    def move(self):
        self.position[0] += int(self.speed * cos(self.bearing))
        self.position[1] += int(self.speed * sin(self.bearing))

    def collide_rect(self, rect, internal):
        """
        rect is a pygame Rect.
        internal says whether we are bouncing around the inside of the
        rectange, or are outside it bouncing agaist it.
        """
        left, top = rect.left, rect.top
        right = rect.left + rect.width
        bottom = rect.top + rect.height
        if internal:
            if self.position[1] - top < self.radius:
                self.bearing *= -1
                self.position[1] = top + self.radius
            if bottom - self.position[1] < self.radius:
                self.bearing *= -1
                self.position[1] = bottom - self.radius
            if self.position[0] - left < self.radius:
                self.bearing = self.bearing * -1 + pi
                self.position[0] = left + self.radius
            if right - self.position[0] < self.radius:
                self.bearing = self.bearing * -1 + pi
                self.position[0] = right - self.radius
        else:  # external
            raise NotImplementedError

        # Condition bearing back into the range -pi to +pi
        while self.bearing < -pi:
            self.bearing += 2*pi
        while self.bearing > pi:
            self.bearing -= 2*pi

        assert isinstance(self.position[0], int)
        assert isinstance(self.position[1], int)


balls = []
balls.append(Ball(**ball_defaults))
screen_rect = pygame.Rect(0, 0, width, height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    balls[0].move()
    balls[0].collide_rect(screen_rect, internal=True)

    screen.fill(background)
    balls[0].draw(screen)
    pygame.display.flip()
