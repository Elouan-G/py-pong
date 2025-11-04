import asyncio
import json
import websockets
from source.pong_server import PongServer


class Server:
    def __init__(self):
        self.players = set()

    async def update_handler(self, game_state: dict):
        """Sends the current game state to all connected players."""
        game_state_msg = {"type": "state", "state": game_state}
        if self.players:
            for player in self.players:
                await player.send(json.dumps(game_state_msg))
                print(f"Sent to {player.remote_address}: {game_state_msg}")

    async def handle_ws_connection(self, websocket):
        self.players.add(websocket)
        print(f"New player connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                data = json.loads(message)
                print(f"Received: {data}")
                await self.handle_message(websocket, data)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.players.remove(websocket)
            print(f"Player disconnected: {websocket.remote_address}")

    async def handle_message(self, websocket: websockets, data: json):
        """Handle messages received from the client."""
        msg_type = data.get("type")
        if msg_type == "ping":
            pong_msg = {"type": "pong"}
            await websocket.send(json.dumps(pong_msg))
            print(f"Sent: {pong_msg}")
        if msg_type == "stop":
            await websocket.close()

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
        """Main server routine."""
        # asyncio.create_task(self.ping_pong())
        game = PongServer(self.update_handler)
        await game.start()
        await self.stop()

    async def start(self):
        async with websockets.serve(self.handle_ws_connection, "localhost", 5739):
            print("Server running on ws://localhost:5739")
            await self.run()

    async def stop(self):
        print("Server stopping...")
        for ws in self.players:
            stop_msg = {"type": "stop"}
            await ws.send(json.dumps(stop_msg))
            print(f"Sent: {stop_msg}")
        print("Server stopped.")


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.start())
