import pygame
import websockets
import json

from source.paddle import Paddle
from source.ball import Ball


class PongClient:
    """Run's a pong client with pygame."""

    def __init__(self, ws: websockets):
        """Initialises pygame and game variables."""
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.websocket = ws

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
        self.stop()

    async def handle_message(self, data: dict):
        """Handle messages received from the server."""
        msg_type = data.get("type")
        if msg_type == "ping":
            pong_msg = {"type": "pong"}
            await self.websocket.send(json.dumps(pong_msg))
            print(f"Sent: {pong_msg}")
        if msg_type == "stop":
            self.running = False
        if msg_type == "state":
            pass

    async def run(self):
        """Main game loop."""
        while self.running:
            try:
                async for message in self.websocket:
                    data = json.loads(message)
                    print(f"Received: {data}")
                    if data.get("type") != "state":
                        await self.handle_message(data)
                    else:
                        # polls for events
                        for event in pygame.event.get():
                            # window's X button pressed
                            if event.type == pygame.QUIT:
                                self.running = False
                                return

                        # update game with received state
                        data = data["state"]
                        self.screen.fill(data["screen"]["bg_color"])
                        self.left_paddle.set_json(data["left_paddle"])
                        self.right_paddle.set_json(data["right_paddle"])
                        self.ball.set_json(data["ball"])

                        pygame.draw.rect(
                            self.screen, self.left_paddle.color, self.left_paddle.rect
                        )
                        pygame.draw.rect(
                            self.screen, self.right_paddle.color, self.right_paddle.rect
                        )
                        pygame.draw.circle(
                            self.screen,
                            self.ball.color,
                            (self.ball.x_pos, self.ball.y_pos),
                            self.ball.radius,
                        )

                        # update display
                        pygame.display.flip()

            except websockets.ConnectionClosed:
                print("Connection closed by server.")
                self.running = False

    def stop(self):
        """Stops the game and quits pygame."""
        self.running = False
        pygame.quit()
