import asyncio
import websockets


async def handler(websocket):
    async for message in websocket:
        print(f"Received: {message}")
        if message == "ping":
            await websocket.send("pong")


async def main():
    async with websockets.connect("ws://localhost:5739") as ws:
        while True:
            await ws.send("ping")
            await asyncio.sleep(1)
            reply = await ws.recv()
            print(reply)


if __name__ == "__main__":
    asyncio.run(main())
