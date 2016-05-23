from coloredlogs import install

from config import SERVICE
from asyncio import get_event_loop


async def run():
    async with SERVICE as beam:
        await beam._authenticate()
        await beam.read()

install(level="DEBUG")

get_event_loop().run_until_complete(run())
