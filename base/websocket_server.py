import asyncio
import websockets

from abc import ABC, abstractmethod


class WebsocketServer(ABC):
    """"
        Base Object for a websocket server
    """
    BASE_URL = ''
    PORT = int()

    def __init__(self):
        self.websocket = None

    @abstractmethod
    async def handler(cls):
        """
            Method supplied to websocket to interface
        """
        pass

    @classmethod
    def get_url(cls):
        return 'ws://{}:{}'.format(cls.BASE_URL, cls.PORT)

    @classmethod
    def run(cls):
        cls.websocket = websockets.serve(cls.handler, cls.BASE_URL, cls.PORT)
        asyncio.get_event_loop().run_until_complete(cls.websocket)
        asyncio.get_event_loop().run_forever()
