import pygame
import asyncio

from source.paddle import Paddle
from source.ball import Ball


class PongServer:
    """Run's a pong game with pygame."""

    def __init__(self):
        """Initialises pygame and game variables."""
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    async def start(self):
        """Initialises a game and starts the main game loop."""
        # paddles setup
        self.paddle_speed = 500
        self.left_paddle = Paddle(
            self.screen.get_width(), self.screen.get_height(), "left"
        )
        self.right_paddle = Paddle(
            self.screen.get_width(), self.screen.get_height(), "right"
        )

        # ball setup
        self.ball_speed = 300
        self.ball = Ball(
            self.screen.get_width(),
            self.screen.get_height(),
            self.left_paddle,
            self.right_paddle,
        )

        await self.run()

    async def run(self):
        """Main game loop."""
        while self.running:
            # polls for events
            for event in pygame.event.get():
                # window's X button pressed
                if event.type == pygame.QUIT:
                    self.running = False

            # fills the screen to reset the frame
            self.screen.fill("black")

            pygame.draw.rect(self.screen, self.left_paddle.color, self.left_paddle.rect)
            pygame.draw.rect(
                self.screen, self.right_paddle.color, self.right_paddle.rect
            )
            pygame.draw.circle(
                self.screen,
                self.ball.color,
                (self.ball.x_pos, self.ball.y_pos),
                self.ball.radius,
            )

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                self.left_paddle.move(-self.paddle_speed * self.dt)
            if keys[pygame.K_s]:
                self.left_paddle.move(self.paddle_speed * self.dt)
            if keys[pygame.K_UP]:
                self.right_paddle.move(-self.paddle_speed * self.dt)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(self.paddle_speed * self.dt)

            self.ball.move(self.ball_speed * self.dt)

            # updates display
            pygame.display.flip()

            # limits FPS to 60 (dt is delta time in seconds since last frame)
            # dt allows frame-independent movement speed
            await asyncio.sleep(1 / 120)
            self.dt = self.clock.tick(60) / 1000

    def stop(self):
        """Stops the game and quits pygame."""
        self.running = False
        pygame.quit()
