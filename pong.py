import pygame

# pygame's setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# paddles setup
paddle_width = 20
paddle_height = 60
paddle_left = pygame.Rect(
    screen.get_width() / 7 - paddle_width / 2,
    screen.get_height() / 2 - paddle_height / 2,
    paddle_width,
    paddle_height,
)
paddle_right = pygame.Rect(
    screen.get_width() / 7 * 6 - paddle_width / 2,
    screen.get_height() / 2 - paddle_height / 2,
    paddle_width,
    paddle_height,
)

while running:
    # polls for events
    for event in pygame.event.get():
        # window's X button pressed
        if event.type == pygame.QUIT:
            running = False

    # fills the screen to reset the frame
    screen.fill("black")

    pygame.draw.rect(screen, "red", paddle_left)
    pygame.draw.rect(screen, "blue", paddle_right)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        paddle_left.move_ip(0, -300 * dt)
    if keys[pygame.K_s]:
        paddle_left.move_ip(0, 300 * dt)
    if keys[pygame.K_UP]:
        paddle_right.move_ip(0, -300 * dt)
    if keys[pygame.K_DOWN]:
        paddle_right.move_ip(0, 300 * dt)

    # updates display
    pygame.display.flip()

    # limits FPS to 60 (dt is delta time in seconds since last frame)
    # dt allows frame-independent movement speed
    dt = clock.tick(60) / 1000

pygame.quit()
