import pygame
from math import sin, cos, pi
import os


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
        self.sprite = pygame.image.load(
            os.path.join("images", "ball_{}.png".format(radius)))
        if self.sprite.get_size() != (2*radius, 2*radius):
            raise RuntimeError("Ball sprite is the wrong size.")

    def draw(self, surface, pos=None):
        # Blit's position argument is the top-left of the sprite
        # whereas self.position is the centre.
        if pos is None:
            surface.blit(self.sprite, (self.position[0] - self.radius,
                                       self.position[1] - self.radius))
        else:
            surface.blit(self.sprite, pos)

    def move(self, dt):
        """
        dt is the time which has passed, in milliseconds, since the last time
        ball.move was called.  This means even if your computer chugs at a low
        fps the ball should still move at the same speed
        """
        speed_adj = self.speed * dt / (1000.0 / 50)
        self.position[0] += int(speed_adj * cos(self.bearing))
        self.position[1] += int(speed_adj * sin(self.bearing))

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
        Returns true if a bounce occurred, else False
        """
        bounce = False
        if self.position[1] - rect.top < self.radius:
            # Bounce top edge
            self.bearing *= -1
            self.position[1] = rect.top + self.radius
            bounce = True
        if rect.bottom - self.position[1] < self.radius:
            # Bounce bottom edge
            self.bearing *= -1
            self.position[1] = rect.bottom - self.radius
            bounce = True
        if self.position[0] - rect.left < self.radius:
            # Bounce left edge
            self.bearing = self.bearing * -1 + pi
            self.position[0] = rect.left + self.radius
            bounce = True
        if rect.right - self.position[0] < self.radius:
            # Bounce right edge
            self.bearing = self.bearing * -1 + pi
            self.position[0] = rect.right - self.radius
            bounce = True
        self.condition_bearing()
        return bounce

    def collide_rect_external(self, rect):
        """
        rect is a pygame Rect.
        Use this method when we are bouncing against the outside of a rectangle
        Returns true if a bounce occurred, else False
        """
        bounce = False
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
                bounce = True
            elif (self.position[1] - rect.bottom < self.radius
                    and self.position[1] - rect.bottom > 0):
                # Bounce bottom edge
                self.bearing *= -1
                self.position[1] = rect.bottom + self.radius
                bounce = True

        # Check if we should collide against the left or right edges
        if (self.position[1] > rect.top - self.radius
                and self.position[1] < rect.bottom):
            if (rect.left - self.position[0] < self.radius
                    and rect.left - self.position[0] > 0):
                # Bounce left edge
                self.bearing = self.bearing * -1 + pi
                self.position[0] = rect.left - self.radius
                bounce = True
            elif (self.position[0] - rect.right < self.radius
                    and self.position[0] - rect.left > 0):
                # Bounce right edge
                self.bearing = self.bearing * -1 + pi
                self.position[0] = rect.right + self.radius
                bounce = True
        self.condition_bearing()
        return bounce
