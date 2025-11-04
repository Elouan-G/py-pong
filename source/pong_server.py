import pygame
import asyncio

from source.paddle import Paddle
from source.ball import Ball


class PongServer:
    """Run's a pong game with pygame."""

    def __init__(self, update_handler):
        """Initialises pygame and game variables."""
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.update_handler = update_handler

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

        # screen setup
        self.bg_color = "black"

        await self.run()
        self.stop()

    async def run(self):
        """Main game loop."""
        while self.running:
            # polls for events
            for event in pygame.event.get():
                # window's X button pressed
                if event.type == pygame.QUIT:
                    self.running = False

            # Move objects depending on imput
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
            self.screen.fill(self.bg_color)

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

            pygame.display.flip()

            # update client
            game_state = {
                "left_paddle": self.left_paddle.get_json(),
                "right_paddle": self.right_paddle.get_json(),
                "ball": self.ball.get_json(),
                "screen": {
                    "width": self.screen.get_width(),
                    "height": self.screen.get_height(),
                    "bg_color": self.bg_color,
                },
            }
            await self.update_handler(game_state)

            # limits FPS to 60 (dt is delta time in seconds since last frame)
            # dt allows frame-independent movement speed
            await asyncio.sleep(1 / 60)
            self.dt = self.clock.tick(60) / 1000

    def stop(self):
        """Stops the game and quits pygame."""
        self.running = False
        pygame.quit()
