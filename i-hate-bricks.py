import sys
import pygame
from math import sin, cos, pi

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
ball_defaults = {'position': [50, 50],
                 'bearing': -0.7,
                 'speed': 10,
                 'radius': 50,
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

    def condition_bearing(self):
        """
        Ensure the bearing is in the range -pi to pi
        """
        while self.bearing < -pi:
            self.bearing += 2*pi
        while self.bearing > pi:
            self.bearing -= 2*pi

    def collide_rect_internal(self, rect):
        """
        rect is a pygame Rect.
        Use this method when we are bouncing around inside the rectangle
        """
        if self.position[1] - rect.top < self.radius:
            # Bounce top edge
            self.bearing *= -1
            self.position[1] = rect.top + self.radius
        if rect.bottom - self.position[1] < self.radius:
            # Bounce bottom edge
            self.bearing *= -1
            self.position[1] = rect.bottom - self.radius
        if self.position[0] - rect.left < self.radius:
            # Bounce left edge
            self.bearing = self.bearing * -1 + pi
            self.position[0] = rect.left + self.radius
        if rect.right - self.position[0] < self.radius:
            # Bounce right edge
            self.bearing = self.bearing * -1 + pi
            self.position[0] = rect.right - self.radius
        self.condition_bearing()

    def collide_rect_external(self, rect):
        """
        rect is a pygame Rect.
        Use this method when we are bouncing against the outside of a rectangle
        """
        # If we end up inside the rectangle this collision detection breaks
        # down horribly.
        if (self.position[0] > rect.left and self.position[0] < rect.right
                and self.position[1] > rect.top
                and self.position[1] < rect.bottom):
            raise RuntimeError("Cannot resolve external collision with a ball "
                               "inside a rectangle.")

        # Collision between a ball and the outside of a rectangle is
        # surprisingly complicated.  In the simple 2d simulation the incident
        # angle equals the reflected angle, both normal to the reflecting
        # plane.  This breaks down on a corner, because the angle of the
        # reflecting plane is undefined.  So instead we just simulate the
        # centre point of the ball reflecting off a rectangle enlarged by the
        # radius of the circle.
        # A more interesting simulation would be to give the enlarged rectangle
        # radiused corners, with the same radius as the ball.  Then you get
        # interesting reflection angles if the ball reflects off the corner of
        # the rectangle.  It's unclear how canonical Breakout handles this.

        # Check if we should collide against the top or bottom edges
        if (self.position[0] > rect.left - self.radius
                and self.position[0] < rect.right + self.radius):
            if (rect.top - self.position[1] < self.radius
                    and rect.top - self.position[1] > 0):
                # Bounce top edge
                self.bearing *= -1
                self.position[1] = rect.top - self.radius
            elif (self.position[1] - rect.bottom < self.radius
                    and self.position[1] - rect.bottom > 0):
                # Bounce bottom edge
                self.bearing *= -1
                self.position[1] = rect.bottom + self.radius

        # Check if we should collide against the left or right edges
        if (self.position[1] > rect.top - self.radius
                and self.position[1] < rect.bottom):
            if (rect.left - self.position[0] < self.radius
                    and rect.left - self.position[0] > 0):
                # Bounce left edge
                self.bearing = self.bearing * -1 + pi
                self.position[0] = rect.left - self.radius
            elif (self.position[0] - rect.right < self.radius
                    and self.position[0] - rect.left > 0):
                # Bounce right edge
                self.bearing = self.bearing * -1 + pi
                self.position[0] = rect.right + self.radius
        self.condition_bearing()


balls = []
balls.append(Ball(**ball_defaults))
screen_rect = pygame.Rect(0, 0, width, height)

box = pygame.Rect(300, 300, 300, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    balls[0].move()
    balls[0].collide_rect_internal(screen_rect)
    balls[0].collide_rect_external(box)

    screen.fill(background)
    pygame.draw.rect(screen, (255, 255, 255), box)
    balls[0].draw(screen)
    pygame.display.flip()
