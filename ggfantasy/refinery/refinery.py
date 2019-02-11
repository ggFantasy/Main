import websockets
import requests
import asyncio
import os
import json
import sys

from datetime import datetime

from ggfantasy.cipher.cipher import Cipher
from mockups.services.league_mock import LeagueMock
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


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

    def __init__(self, dry_run=False):
        self.raw_data_table = None
        self.processed_data_table = None
        self.connect_to_db()
        self.dry_run = dry_run

    def launch(self):
        print("launching")
        refinery_server = websockets.serve(self.processor, 'localhost', '7777', process_request=self.process_request)
        asyncio.get_event_loop().run_until_complete(refinery_server)
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
            return data['token']
        except Exception as e:
            raise Exception(e)

    def _get_auth_live_stream_url(self):
        return self.LIVE_URL.format(self._get_token())

    def process_event(self, event):
        try:
            # Grabs the first key of the JSON programmatically
            event_key = [*event][0]
            teams = 'teamStats'
            players = 'playerStats'

            # TODO Create other processors to process other events
            # Other processors:
            # Teams
            # Game Initializer - grab champ picks, bans, etc.
            processed_events = dict()
            processed_players = self.process_player_events(event[event_key][players])
            processed_events[event_key] = {
                players: processed_players
            }
            try:
                processed_events[teams] = event[teams]
            except KeyError:
                pass
        except KeyError as e:
            raise Exception(e)
        return processed_events

    def process_player_events(self, players):
        for player in players:
            processed_player = {k: v for k, v in players[player].items() if k in self.KEYS}
            players[player] = processed_player

        return players

    def process_team_events(self, teams):
        for team in teams:
            processed_team = {}

    def process_request(self, path, request_headers):
        if path == "/tests/":
            print("Hit Tests")

    async def processor(self, websocket, path, dry_run=False):
        source = self._get_auth_live_stream_url() if not self.dry_run else LeagueMock.get_url()
        print("source {}".format(source))
        print("path var {}".format(path))
        async with websockets.connect(source) as input_socket:
            # TODO Make this NOT an infinite loop
            # Possibly with <async for message in websocket>
            async for message in input_socket:
                data = await input_socket.recv()
                processed_data = self.process_event(json.loads(data))
                await websocket.send(json.dumps(processed_data))
                # async with websockets.connect(Cipher.get_url()) as cipher:
                # async with websockets.connect('ws://95946837.ngrok.io') as cipher:
                #     await cipher.send(json.dumps(processed_data))

                print('Data: {}'.format(data))
                print('Processed data: {}'.format(processed_data))

                # self.raw_data_table.write('{},\n'.format(data))
                # self.processed_data_table.write('{},\n'.format(json.dumps(processed_data)))


if __name__ == '__main__':
    try:
        dry_run = bool(sys.argv[1])
    except IndexError:
        dry_run = False
    print(dry_run)
    refinery = Refinery(dry_run)
    refinery.launch()
