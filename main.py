import pygame

from source.paddle import Paddle
from source.ball import Ball

# pygame's setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# paddles setup
paddle_speed = 500
left_paddle = Paddle(screen.get_width(), screen.get_height(), "left")
right_paddle = Paddle(screen.get_width(), screen.get_height(), "right")

# ball setup
ball_speed = 300
ball = Ball(screen.get_width(), screen.get_height(), left_paddle, right_paddle)

# main game loop
while running:
    # polls for events
    for event in pygame.event.get():
        # window's X button pressed
        if event.type == pygame.QUIT:
            running = False

    # fills the screen to reset the frame
    screen.fill("black")

    pygame.draw.rect(screen, left_paddle.color, left_paddle.rect)
    pygame.draw.rect(screen, right_paddle.color, right_paddle.rect)
    pygame.draw.circle(screen, ball.color, (ball.x_pos, ball.y_pos), ball.radius)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        left_paddle.move(-paddle_speed * dt)
    if keys[pygame.K_s]:
        left_paddle.move(paddle_speed * dt)
    if keys[pygame.K_UP]:
        right_paddle.move(-paddle_speed * dt)
    if keys[pygame.K_DOWN]:
        right_paddle.move(paddle_speed * dt)

    ball.move(ball_speed * dt)

    # updates display
    pygame.display.flip()

    # limits FPS to 60 (dt is delta time in seconds since last frame)
    # dt allows frame-independent movement speed
    dt = clock.tick(60) / 1000

pygame.quit()
