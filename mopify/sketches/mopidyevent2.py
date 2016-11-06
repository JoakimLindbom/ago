import websocket
import threading
from time import sleep

def on_message(ws, message):
    print message

def on_close(ws):
    print "### closed ###"

def send(method):
    payload = '{\
    "method": "' + method + '",\
    "jsonrpc": "2.0",\
    "params": {},\
    "id": 1\
    }'

    print  payload

    ws.send(payload)
    print "Sent"


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.1.1:6680/mopidy/ws", on_message = on_message, on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
        sleep(1)
        conn_timeout -= 1

    send("core.get_version")

    msg_counter = 0
    while ws.sock.connected:
        print "."

        sleep(5)
        msg_counter += 1
