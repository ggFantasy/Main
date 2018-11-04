import websockets
import requests
import asyncio
import os
import json
import sys

from datetime import datetime

from ggfantasy.cipher.cipher import Cipher
from mockups.services.league_mock import LeagueMock


# TODO Abstract this so each game inherits from base refinery
class Refinery:
    """
        Refinery will receive and process live data, and broadcast processed data
        to upstream consumers.
        Will also store raw and processed data for later use
    """
    LIVE_URL = 'wss://livestats.proxy.lolesports.com/stats?jwt={}'
    JWT_GEN = 'https://api.lolesports.com/api/issueToken'

    # Desired keys when processing events
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

    @staticmethod
    def get_path():
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

    @staticmethod
    def process_event(event):
        try:
            # Grabs the first key of the JSON programmatically
            event_key = [*event][0]

            # TODO Create other processors to process other events
            # Other processors:
            # Teams
            # Game Initializer - grab champ picks, bans, etc.
            players = event[event_key]['playerStats']
            for player in players:
                processed_player = {k: v for k, v in players[player].items() if k in keys}
                players[player] = processed_player
        except KeyError as e:
            raise Exception(e)
        return players

    async def processor(self, dry_run=False):
        source = self._get_auth_live_stream_url() if not dry_run else LeagueMock.get_url()
        async with websockets.connect(source) as websocket:
            # TODO Make this NOT an infinite loop
            # Possibly with <async for message in websocket>
            while True:
                data = await websocket.recv()
                processed_data = self.process_event(json.loads(data))
                async with websockets.connect(Cipher.get_url()) as cipher:
                    await cipher.send(json.dumps(processed_data))

                print('Data: {}'.format(data))
                print('Processed data: {}'.format(processed_data))

                self.raw_data_table.write('{},\n'.format(data))
                self.processed_data_table.write('{},\n'.format(json.dumps(processed_data)))


if __name__ == '__main__':
    try:
        dry_run = bool(sys.argv[1])
    except IndexError:
        dry_run = False
    refinery = Refinery()
    refinery.launch(dry_run)
