#!/usr/bin/python

from websocket import create_connection


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


def rcv():
    print "Receiving..."
    result = ws.recv()
    print "Received '%s'" % result
    return result


if __name__ == "__main__":

    ws = create_connection("ws://192.168.1.1:6680/mopidy/ws")
    print "Sending 1"
    send("core.get_version")
    for i in range(10000):
        print rcv()

    ws.close()
