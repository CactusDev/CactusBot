
import asyncio
from cactusbot.sepal import Sepal


async def run_sepal():
    sepal = Sepal("innectic")
    await sepal.connect()
    await sepal.read(handle)

async def handle(packet):
    print(packet)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sepal())
loop.run_forever()
