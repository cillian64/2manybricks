import sys
import pygame

from ball import Ball
from brick import Brick
from paddle import Paddle

size = width, height = 1024, 768
screen_rect = pygame.Rect(0, 0, width, height)
screen = pygame.display.set_mode(size)
ball_defaults = {'position': [50, 50],
                 'bearing': -0.7,
                 'speed': 10,
                 'radius': 50,
                 'colour': (255, 0, 0)
                 }
background = (0, 0, 0)

balls = []
balls.append(Ball(**ball_defaults))

bricks = []
bricks.append(Brick(pygame.Rect(300, 300, 300, 300), (255, 255, 255), 1))

paddle = Paddle(pygame.Rect(100, height-50, 150, 15), width, (255, 255, 255))

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Move the paddle
    paddle.move(pygame.mouse.get_pos())

    # Handle all the ball movement and collision
    for ball in balls:
        balls[0].collide_rect_internal(screen_rect)
        for brick in bricks:
            if ball.collide_rect_external(brick.rect):
                brick.hit()
        paddle.collide(ball)
        balls[0].move()

    # Remove dead bricks
    bricks = [brick for brick in bricks if brick.alive()]

    # Blank the screen, draw all the bricks, draw the balls
    screen.fill(background)
    for brick in bricks:
        brick.draw(screen)
    for ball in balls:
        ball.draw(screen)
    paddle.draw(screen)

    pygame.display.flip()
