import score
import asyncio
from websockets.server import serve
import fms

m_matchScore = score.MatchScore()

def msgHandler(msg):
    if msg['type'] == 'addScore':
        m_matchScore.addScore(msg['data']['alliance'], msg['data']['location'], msg['data']['score'])
        return 0

async def main() :
    async with serve(msgHandler, 'localhost', 8700) as server:
        await asyncio.Future()

async def sendScore():
    while True:
        m_matchScore.updateArena()
        await asyncio.sleep(0.1)

asyncio.run(main())
asyncio.run(sendScore())