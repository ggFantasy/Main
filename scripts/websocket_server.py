import asyncio
import websockets
import random

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

async def game_events(websocket, path):
    print('here')
    for event in events:
        await websocket.send(event)
        await asyncio.sleep(random.random() * 2)


f = open('10_20_18.txt', 'r')
events = f.readlines()
start_server = websockets.serve(game_events, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
print('there')
asyncio.get_event_loop().run_forever()