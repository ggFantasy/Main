import asyncio
import websockets
import random

from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client.ggf_mockup
collection = db.league_matches




class LeagueMock:
    BASE_URL = 'localhost'
    PORT = '8765'

    def __init__(self):
        self.game = None
        self.websocket = None
        self.connect_to_db()

    def connect_to_db(self):
        game = open('2018-10-27 01:00:23.390713_raw_data.txt', 'r')
        print("Game Opened")
        self.game = game.readlines()

    def run(self):
        print('Running mock websocket')
        self.websocket = websockets.serve(self.emit, self.BASE_URL, self.PORT)
        asyncio.get_event_loop().run_until_complete(self.websocket)
        asyncio.get_event_loop().run_forever()

    @staticmethod
    def get_url():
        return 'ws://{}:{}'.format(LeagueMock.BASE_URL, LeagueMock.PORT)

    async def emit(self, websocket):
        print("Game Events Emitting")
        for event in self.game:
            print(event)
            await websocket.send(event)
            await asyncio.sleep(random.random() * 2)

if __name__ == '__main__':
    pprint.pprint(collection.find_one())
    league_server = LeagueMock()
    league_server.run()
