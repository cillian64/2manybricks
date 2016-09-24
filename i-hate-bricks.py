import sys
from math import pi
import pygame

from ball import Ball
from paddle import Paddle
from levels import load_level, NoMoreLevels


def play_level(level, width, height, sounds):
    screen_rect = pygame.Rect(0, 0, width, height)
    balls = []
    balls.append(Ball([0, 0], pi/2, 10, 15, (255, 0, 0)))
    bricks = load_level(level, width, height)
    paddle = Paddle(pygame.Rect(100, height-50, 150, 15), width,
                    (255, 255, 255))

    sticky_paddle = True
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

        if sticky_paddle:
            balls[0].position[0] = paddle.x
            balls[0].position[1] = (paddle.y - int(paddle.height/2) -
                                    balls[0].radius - 1)
            balls[0].speed = 0
            balls[0].bearing = pi/2
            if pygame.mouse.get_pressed()[0]:
                balls[0].speed = 10
                sticky_paddle = False

        # Handle all the ball movement and collision
        for ball in balls:
            ball.collide_rect_internal(screen_rect)
            for brick in bricks:
                if ball.collide_rect_external(brick.rect):
                    brick.hit()
                    sounds['brick'].play()
            if paddle.collide(ball):
                sounds['paddle'].play()
            ball.move()

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
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode(size)
sounds = {
    'paddle': pygame.mixer.Sound('zap1.wav'),
    'brick': pygame.mixer.Sound('click1.wav'),
}
if len(sys.argv) == 2:
    level = int(sys.argv[1])
else:
    level = 0
while True:
    try:
        play_level(level, width, height, sounds)
    except NoMoreLevels:
        print("You win!")
        sys.exit(0)
    level += 1
