from coloredlogs import install

from config import SERVICE, USERNAME, PASSWORD
from asyncio import get_event_loop


async def run():
    async with SERVICE as beam:
        await beam.run(USERNAME, PASSWORD)

install(level="DEBUG")

loop = get_event_loop()
try:
    loop.run_until_complete(run())
finally:
    loop.close()
