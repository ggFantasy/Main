import websocket
import requests
try:
    import thread
except ImportError:
    import _thread as thread
import time

jwt_generator = 'https://api.lolesports.com/api/issueToken'

def on_message(ws, message):
    print(message)
    f.write("\n\nMessage: {}\n\n".format(message))


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        '''for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        '''
        print("thread terminating...")
    thread.start_new_thread(run, ())

def get_token():
    resp = requests.get(jwt_generator)
    data = resp.json()
    try:
        return data['token']
    except Exception:
        raise Exception

if __name__ == "__main__":
    f = open('live_data_match_2.txt', 'a')
    websocket.enableTrace(True)
    token = get_token()
    route = "wss://livestats.proxy.lolesports.com/stats?jwt={}".format(token)
    # route = 'ws://localhost:8765'
    # websocket.create_connection(route)
    ws = websocket.WebSocketApp(route,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()