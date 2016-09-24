import sys
from math import pi
import pygame

from ball import Ball
from paddle import Paddle
from levels import load_level, NoMoreLevels


def play_level(level, width, height):
    screen_rect = pygame.Rect(0, 0, width, height)
    balls = []
    balls.append(Ball([0, 0], pi/2, 10, 15, (255, 0, 0)))
    bricks = load_level(level, width, height)
    paddle = Paddle(pygame.Rect(100, height-50, 150, 15), width,
                    (255, 255, 255))

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Destroy balls which escape the bottom:
        balls = [ball for ball in balls
                 if ball.position[1] < height - ball.radius]

        # If there are no balls left, we lost!
        if len(balls) == 0:
            print("You lose!")
            sys.exit(0)

        # If there are no bricks left, you cleared this level
        if len(bricks) == 0:
            print("Level {} cleared.".format(level))
            return

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
        screen.fill((0, 0, 50))
        for brick in bricks:
            brick.draw(screen)
        for ball in balls:
            ball.draw(screen)
        paddle.draw(screen)

        pygame.display.flip()


size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
level = 0
while True:
    try:
        play_level(level, width, height)
    except NoMoreLevels:
        print("You win!")
        sys.exit(0)
    level += 1
