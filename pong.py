import pygame

from source.paddle import Paddle

# pygame's setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# paddles setup
paddle_width = 20
paddle_height = 60
left_paddle = Paddle(
    screen.get_width(), screen.get_height(), "left", paddle_width, paddle_height
)
right_paddle = Paddle(
    screen.get_width(), screen.get_height(), "right", paddle_width, paddle_height
)

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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        left_paddle.move(-300 * dt)
    if keys[pygame.K_s]:
        left_paddle.move(300 * dt)
    if keys[pygame.K_UP]:
        right_paddle.move(-300 * dt)
    if keys[pygame.K_DOWN]:
        right_paddle.move(300 * dt)

    # updates display
    pygame.display.flip()

    # limits FPS to 60 (dt is delta time in seconds since last frame)
    # dt allows frame-independent movement speed
    dt = clock.tick(60) / 1000

pygame.quit()
