import json
import threading
import score
import websockets
import asyncio
import fms
from time import sleep

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
            message = json.loads(message)
            if message['type'] == 'addScore':
                m_matchScore.addScore(message["data"]["alliance"], m_match.state, message["data"]["score"])
                print(str(m_matchScore.redAuto))
                print(str(m_matchScore.redTeleop))
                print(str(m_matchScore.redEndgame))
                print(str(m_matchScore.blueAuto))
                print(str(m_matchScore.blueTeleop))
                print(str(m_matchScore.blueEndgame))

def sendScore():
    while True:
        m_matchScore.updateArena()
        sleep(1)

scoreUpdater = threading.Thread(target=sendScore)

def updateState():
    while True:
        curr_state = fms.timeHandler()
        if curr_state == 0:
            continue
        m_match.state = curr_state['data']['MatchState']
        # print(m_match.state)
        sleep(1)

stateUpdater = threading.Thread(target=updateState)

def reset():
    while True:
        if m_match.state == 0 or m_match.state == 6:
            m_matchScore.reset()
            sleep(1)
            # print('reset' + str(m_match.state))

resetUpdater = threading.Thread(target=reset)

async def main():
    async with websockets.serve(handler, "", 8700):
        await asyncio.Future()  # run forever

fms.initConnections()
stateUpdater.start()
resetUpdater.start()
scoreUpdater.start()
asyncio.run(main())