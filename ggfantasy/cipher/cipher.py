
import asyncio
import websockets
from datetime import datetime


async def listen_for_events(websocket, path):
    async for message in websocket:
        print("Event {}".format(message))


if __name__ == '__main__':
    start_server = websockets.serve(listen_for_events, 'localhost', 9734)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
