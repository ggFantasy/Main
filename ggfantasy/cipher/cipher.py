import asyncio
import websockets


class Cipher:
    BASE_URL = 'localhost'
    PORT = 9734

    def __init__(self):
        self.websocket = None

    @staticmethod
    def get_url():
        return 'ws://{}:{}'.format(Cipher.BASE_URL, Cipher.PORT)

    async def receiver(self, websocket, path):
        async for message in websocket:
            print('Event {}'.format(message))

    def run(self):
        print('Launching Cipher...')
        self.websocket = websockets.serve(self.receiver, self.BASE_URL, self.PORT)
        asyncio.get_event_loop().run_until_complete(self.websocket)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    cipher = Cipher()
    cipher.run()
