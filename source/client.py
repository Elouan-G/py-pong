import asyncio
import json
import websockets


class PongClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket = None
        self.running = True

    async def connect(self):
        """Connect to the WebSocket server."""
        print(f"Connecting to {self.uri}...")
        self.websocket = await websockets.connect(self.uri)
        print("Connected to server.")

    async def listen(self):
        """Listen for messages from the server."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                print("Received:", data)
                await self.handle_message(data)
        except websockets.ConnectionClosed:
            print("Connection closed by server.")
            self.running = False

    async def handle_message(self, data: dict):
        """Handle messages received from the server."""
        msg_type = data.get("type")
        if msg_type == "ping":
            await self.send({"type": "pong"})

    async def send(self, data: dict):
        """Send a JSON message to the server."""
        if self.running and self.websocket:
            await self.websocket.send(json.dumps(data))
            print(f"Sent: {data}")

    async def ping_pong(self):
        while self.running:
            if self.websocket:
                ping_msg = {"type": "ping"}
                await self.send(ping_msg)
                print(f"Sent: {ping_msg}")
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(5)

    async def run(self):
        """Main entry point."""
        while self.running:
            try:
                await self.connect()
            except (OSError, websockets.InvalidURI, websockets.InvalidHandshake):
                print("Failed to connect, retrying in 3s...")
                await asyncio.sleep(3)
            else:
                await asyncio.gather(self.listen(), self.ping_pong())


if __name__ == "__main__":
    client = PongClient("ws://localhost:5739")
    asyncio.run(client.run())
