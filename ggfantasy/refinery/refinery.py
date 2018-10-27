"""
    Processor for Live Data from League of Legends websocket
"""
import websockets
import requests
import asyncio
import json

from datetime import datetime

live_stream = 'wss://livestats.proxy.lolesports.com/stats?jwt={}'
# live_stream = 'ws://localhost:8765'
# live_stream = 'wss://livestats.proxy.lolesports.com/stats?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2IjoiMS4wIiwiamlkIjoiMTcwZjU1YzEtNDA2ZC00YjhkLTgzZDctNGFkNDliNmNhZjlhIiwiaWF0IjoxNTQwNjI2NjA4NTIwLCJleHAiOjE1NDEyMzE0MDg1MjAsIm5iZiI6MTU0MDYyNjYwODUyMCwiY2lkIjoiYTkyNjQwZjI2ZGMzZTM1NGI0MDIwMjZhMjA3NWNiZjMiLCJzdWIiOnsiaXAiOiI5OC4yMTAuMTM3LjQwIiwidWEiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xM180KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjEwMCBTYWZhcmkvNTM3LjM2In0sInJlZiI6WyJ3YXRjaC4qLmxvbGVzcG9ydHMuY29tIl0sInNydiI6WyJsaXZlc3RhdHMtdjEuMCJdfQ.W0CXFR2Cg-b26iZ3tfick0Ar0MvEUr9z98_wZgpeTKk'
our_websocket = 'ws://localhost:9734'
jwt_generator = 'https://api.lolesports.com/api/issueToken'

# "kills": 2,
#  "deaths": 1,
#  "assists": 7,
#  "doubleKills": 0,
#  "tripleKills": 0,
#  "quadraKills": 0,
#  "pentaKills": 0,
# "mk": 233

keys = ['kills', 'deaths', 'assists', 'doubleKills', 'tripleKills', 'quadraKills', 'pentaKills', 'mk']

def get_token():
    resp = requests.get(jwt_generator)
    data = resp.json()
    try:
        print("Token: {}".format(data['token']))
        return data['token']
    except Exception:
        raise Exception

def process_event(event):
    players = list()
    try:
        event_key = [*event][0]
        players = event[event_key]['playerStats']
        for player in players:
            processed_player = {k: v for k, v in players[player].items() if k in keys}
            players[player] = processed_player
    except Exception as e:
        pass
    return players

async def open_connection():
    token = get_token()
    async with websockets.connect(live_stream.format(token)) as websocket:
    # async with websockets.connect(live_stream) as websocket:
        # async for message in websocket:
        while True:
            data = await websocket.recv()
            processed_data = process_event(json.loads(data))
            async with websockets.connect(our_websocket) as gg_socket:
                await gg_socket.send(json.dumps(processed_data))
            print('Data: {}'.format(data))
            print('Processed data: {}'.format(processed_data))
            f1.write('{},\n'.format(data))
            f2.write('{},\n'.format(json.dumps(processed_data)))

if __name__ == '__main__':
    now = datetime.now()
    f1 = open('{}_raw_data.txt'.format(now), 'w')
    f2 = open('{}_data_from_cipher.txt'.format(now), 'w')
    asyncio.get_event_loop().run_until_complete(open_connection())
    asyncio.get_event_loop().run_forever()
