import random

from asyncio import sleep
from pymongo import MongoClient

from base.websocket_server import WebsocketServer

client = MongoClient('localhost', 27017)
db = client.ggf_mockup
collection = db.league_matches


class LeagueMock(WebsocketServer):
    """
        Mock Websocket to emit data from previous live games
    """
    BASE_URL = 'localhost'
    PORT = '8765'

    def __init__(self):
        self.game = None
        self.connect_to_db()
        super(LeagueMock, self).__init__()

    @classmethod
    async def handler(cls, websocket, path):
        print("Game Events Emitting")
        for event in cls.game:
            print(event)
            await websocket.send(event)
            await sleep(random.random() * 2)

    @classmethod
    def connect_to_db(cls):
        game = open('10_20_18.txt', 'r')
        print("Game Opened")
        cls.game = game.readlines()


if __name__ == '__main__':
    league_server = LeagueMock()
    league_server.run()
