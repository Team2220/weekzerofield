import asyncio
from websockets.server import serve

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

async def echo(websocket):
    async for message in websocket:
        print(message)

async def main():
    async with serve(echo, "localhost", 8700):
        await asyncio.Future()  # run forever

asyncio.run(main())