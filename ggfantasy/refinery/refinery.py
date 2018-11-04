"""
    Processor for Live Data from League of Legends websocket
"""
import websockets
import requests
import asyncio
import os
import json
import sys

from datetime import datetime

from ggfantasy.cipher.cipher import Cipher
from mockups.services.league_mock import LeagueMock

live_stream = 'wss://livestats.proxy.lolesports.com/stats?jwt={}'
# live_stream = 'ws://localhost:8765'
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


# Should have a base refinery and have each game inherit from it
class Refinery:
    """
        Refinery will receive and process live data, and broadcast processed data
        to upstream consumers.
        Will also store raw and processed data for later use
    """
    LIVE_URL = 'wss://livestats.proxy.lolesports.com/stats?jwt={}'
    JWT_GEN = 'https://api.lolesports.com/api/issueToken'

    KEYS = [
        'kills',
        'deaths',
        'assists',
        'doubleKills',
        'tripleKills',
        'quadraKills',
        'pentaKills',
        'mk'
    ]

    def __init__(self):
        self.raw_data_table = None
        self.processed_data_table = None
        self.connect_to_db()

    def launch(self, dry_run=False):
        asyncio.get_event_loop().run_until_complete(self.processor(dry_run))
        asyncio.get_event_loop().run_forever()


    def connect_to_db(self):
        now = datetime.now()
        self.raw_data_table = open('{}_raw_data.txt'.format(now), 'w')
        self.processed_data_table = open('{}_processed_data.txt'.format(now), 'w')

    def get_path(self):
        return os.path.dirname(os.path.abspath(__file__))

    def _get_token(self):
        resp = requests.get(self.JWT_GEN)
        data = resp.json()
        try:
            return data['token ']
        except Exception as e:
            raise Exception(e)

    def _get_auth_live_stream_url(self):
        return self.LIVE_URL.format(self._get_token())

    def process_event(self, event):
        players = dict()
        try:
            # Grabs the first key of the JSON programmatically
            event_key = [*event][0]

            # Here we should be grabbing other events like team events
            # Then send them into their own processors
            players = event[event_key]['playerStats']
            for player in players:
                processed_player = {k: v for k, v in players[player].items() if k in keys}
                players[player] = processed_player

        except KeyError as e:
            raise Exception(e)
        return players

    async def processor(self, dry_run=False):
        # TODO Import LeagueMock
        # TODO Create a Mock directory for different mock services
        source = self._get_auth_live_stream_url() if not dry_run else LeagueMock.get_url()
        print("Source: {}".format(source))
        async with websockets.connect(source) as websocket:
            # Make this NOT an infinite loop
            # Possibly with <async for message in websocket>
            while True:
                data = await websocket.recv()
                print(data)
                processed_data = process_event(json.loads(data))
                async with websockets.connect(Cipher.get_url()) as cipher:
                    await cipher.send(json.dumps(processed_data))

                print('Data: {}'.format(data))
                print('Processed data: {}'.format(processed_data))

                self.raw_data_table.write('{},\n'.format(data))
                self.processed_data_table.write('{},\n'.format(json.dumps(processed_data)))


if __name__ == '__main__':
    try:
        dry_run  = bool(sys.argv[1])
    except IndexError:
        dry_run = False
    refinery = Refinery()
    refinery.launch(dry_run)
