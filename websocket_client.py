import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

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


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://livestats.proxy.lolesports.com/stats?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2IjoiMS4wIiwiamlkIjoiNzNmMTc1ZWEtZjUwMC00NmU2LWIxYmMtNTQ1YjIzZjU5ZTc1IiwiaWF0IjoxNTM5NzYzNzcwNzE0LCJleHAiOjE1NDAzNjg1NzA3MTQsIm5iZiI6MTUzOTc2Mzc3MDcxNCwiY2lkIjoiYTkyNjQwZjI2ZGMzZTM1NGI0MDIwMjZhMjA3NWNiZjMiLCJzdWIiOnsiaXAiOiI5OC4yMTAuMTM3LjQwIiwidWEiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xM180KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjEwMCBTYWZhcmkvNTM3LjM2In0sInJlZiI6WyJ3YXRjaC4qLmxvbGVzcG9ydHMuY29tIl0sInNydiI6WyJsaXZlc3RhdHMtdjEuMCJdfQ.ApbWyChSDGELLtXRhhGszrWk1f0XJbfVEUq2d72nusk",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()