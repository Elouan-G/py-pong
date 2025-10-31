import asyncio
import json
import websockets


class PongServer:
    def __init__(self):
        self.players = set()

    async def handler(self, websocket):
        self.players.add(websocket)
        print("New player connected!")

        try:
            async for message in websocket:
                data = json.loads(message)
                print("Received:", data)
                await self.handle_message(websocket, data)
        except websockets.ConnectionClosed:
            print("Player disconnected")
        finally:
            self.players.remove(websocket)

    async def handle_message(self, websocket: websockets, data: json):
        """Handle messages received from the client."""
        msg_type = data.get("type")
        if msg_type == "ping":
            pong_msg = {"type": "pong"}
            await websocket.send(json.dumps(pong_msg))
            print(f"Sent: {pong_msg}")

    async def ping_pong(self):
        while True:
            if self.players:
                ping_msg = {"type": "ping"}
                for player in self.players:
                    await player.send(json.dumps(ping_msg))
                    print(f"Sent: {ping_msg}")
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(5)

    async def run(self):
        async with websockets.serve(self.handler, "localhost", 5739):
            await self.ping_pong()


if __name__ == "__main__":
    server = PongServer()
    asyncio.run(server.run())
