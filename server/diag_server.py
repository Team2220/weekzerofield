import websocket
from time import sleep

ws = websocket.WebSocket()
wsURL = "ws://127.0.0.1:8080/match_play/websocket"

def initConnections() :
    ws.connect(wsURL)

initConnections()

# keep running
while True:
    print(ws.recv())