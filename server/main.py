import threading
import score
import websockets
import asyncio
import fms

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

m_matchScore = score.MatchScore()

class Match:
    state = 0
    
    def __init__(self):
        self.state = 0

m_match = Match()

async def handler(websocket):
    while True:
        async for message in websocket:
            print(message)

def sendScore():
    while True:
        m_matchScore.updateArena()

scoreUpdater = threading.Thread(target=sendScore)

def updateState():
    while True:
        curr_state = fms.timeHandler()
        print(m_match.state)
        if curr_state == 0:
            continue
        m_match.matchState = curr_state['data']['MatchState']

stateUpdater = threading.Thread(target=updateState)

def reset():
    while True:
        if m_match.state == 0 or m_match.state == 6:
            m_matchScore.reset()

resetUpdater = threading.Thread(target=reset)

async def main():
    async with websockets.serve(handler, "", 8700):
        await asyncio.Future()  # run forever

fms.initConnections()
stateUpdater.start()
resetUpdater.start()
scoreUpdater.start()
asyncio.run(main())