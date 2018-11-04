from base.websocket_server import WebsocketServer


class Cipher(WebsocketServer):
    """
        Cipher is the gateway between our live stream refinery and our front end
        It will emit processed data for the front end to consume
    """
    BASE_URL = 'localhost'
    PORT = 9734

    @classmethod
    async def handler(cls, websocket, path):
        async for message in websocket:
            # Where Cipher should be relaying processed data to front end
            print('Event {}'.format(message))


if __name__ == '__main__':
    cipher = Cipher()
    cipher.run()
