import score
import asyncio
from websockets.server import serve
import fms

m_matchScore = score.MatchScore()

class Match:
    state = 0
    
    def __init__(self):
        self.state = 0

def msgHandler(msg):
    if msg['type'] == 'addScore':
        m_matchScore.addScore(msg['data']['alliance'], msg['data']['state'], msg['data']['score'])
        print('The ' + msg['data']['alliance'] + ' alliance scored ' + str(msg['data']['score']) + ' points in ' + msg['data']['location'] + '.')
        return 0
    else :
        print('Error: Invalid message type: ' + msg['type'])

async def main() :
    async with serve(msgHandler, 'localhost', 8700) as server:
        await asyncio.Future()

async def sendScore():
    while True:
        m_matchScore.updateArena()
        await asyncio.sleep(0.1)

asyncio.run(main())
asyncio.run(sendScore())