import asyncio
import websockets


async def handler(websocket):
    async for message in websocket:
        print(f"Received: {message}")
        if message == "ping":
            await websocket.send("pong")


async def main():
    async with websockets.serve(handler, "localhost", 5739):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
