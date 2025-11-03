import asyncio
import json
import websockets


class PongClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket = None
        self.running = False

    async def ping_pong(self):
        while self.running:
            if self.websocket:
                ping_msg = {"type": "ping"}
                await websockets.send(json.dumps(ping_msg))
                print(f"Sent: {ping_msg}")
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(5)

    async def handle_message(self, data: dict):
        """Handle messages received from the server."""
        msg_type = data.get("type")
        if msg_type == "ping":
            pong_msg = {"type": "pong"}
            await websockets.send(json.dumps(pong_msg))
            print(f"Sent: {pong_msg}")

    async def listen(self):
        """Listen for messages from the server."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                print(f"Received: {data}")
                await self.handle_message(data)
        except websockets.ConnectionClosed:
            print("Connection closed by server.")
            self.running = False

    async def run(self):
        """Main client routine."""
        while self.running:
            listen = asyncio.create_task(self.listen())
            asyncio.create_task(self.ping_pong())
            await listen

    async def connect(self):
        """Connect to the WebSocket server."""
        print(f"Connecting to {self.uri}...")
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to server as {self.websocket.local_address}")

    async def start(self):
        """Connects to the server with retries."""
        wait_time = 5
        for attempt in range(10):
            try:
                await self.connect()
            except (OSError, websockets.InvalidURI, websockets.InvalidHandshake):
                print(
                    f"Connection attempt {attempt + 1} failed, retrying in {wait_time} seconds..."
                )
                await asyncio.sleep(wait_time)
            else:
                self.running = True
                await self.run()


if __name__ == "__main__":
    client = PongClient("ws://localhost:5739")
    asyncio.run(client.start())
