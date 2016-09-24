import sys
from math import pi
import os
import pygame

from ball import Ball
from paddle import Paddle
from levels import load_level, NoMoreLevels


def play_level(level, width, height, sounds, fps, score):
    screen_rect = pygame.Rect(0, 0, width, height)
    balls = []
    balls.append(Ball([0, 0], pi/2, 10, 15, (255, 0, 0)))
    bricks = load_level(level, width, height)
    paddle = Paddle(pygame.Rect(100, height-50, 150, 15), width,
                    (255, 255, 255))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    sticky_paddle = True
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Limit the loop speed to `fps` frames per second
        clock.tick(fps)
        actual_fps = clock.get_fps()
        dt = (1000.0 / actual_fps) if actual_fps > 0 else 0

        # If we have more than one ball, destroy any that reach the bottom
        if len(balls) > 1:
            balls = [ball for ball in balls
                     if ball.position[1] < height - ball.radius]
        elif len(balls) == 1:
            if balls[0].position[1] > height - balls[0].radius:
                # If we only have one ball left and it reaches the bottom,
                # reset our score and sticky the ball/paddle
                sticky_paddle = True
                score = 0
        else:
            raise RuntimeError("Ran out of balls...")

        # If there are no bricks left (except immortal bricks), you cleared
        # this level
        if len([brick for brick in bricks if brick.life > 0]) == 0:
            print("Level {} cleared.".format(level))
            return score

        # Move the paddle
        paddle.move(pygame.mouse.get_pos())

        if sticky_paddle:
            balls[0].position[0] = paddle.x
            balls[0].position[1] = (paddle.y - int(paddle.height/2) -
                                    balls[0].radius - 1)
            balls[0].speed = 0
            balls[0].bearing = -pi/2
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
                    if brick.life != -1:
                        score += 1
            if paddle.collide(ball):
                sounds['paddle'].play()
            ball.move(dt)

        # Remove dead bricks
        bricks = [brick for brick in bricks if brick.alive()]

        # Blank the screen, draw all the bricks, draw the balls
        screen.fill((0, 0, 50))
        for brick in bricks:
            brick.draw(screen)
        for ball in balls:
            ball.draw(screen)
        paddle.draw(screen)
        score_surf = font.render(str(score), 1, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()


size = width, height = 1024, 768
fps = 60  # Frames per second
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode(size)
sounds = {
    'paddle': pygame.mixer.Sound(os.path.join('sounds', 'zap1.wav')),
    'brick': pygame.mixer.Sound(os.path.join('sounds', 'click1.wav')),
}
try:
    pygame.mixer.music.load(os.path.join('sounds', '2manycooks.ogg'))
    pygame.mixer.music.play(loops=-1)
except Exception as e:
    print("Music file not found or libvorbis not installed.")

if len(sys.argv) == 2:
    level = int(sys.argv[1])
else:
    level = 0
score = 0
while True:
    try:
        score = play_level(level, width, height, sounds, fps, score)
    except NoMoreLevels:
        print("You win!")
        print("Score: {}".format(score))
        sys.exit(0)
    level += 1
