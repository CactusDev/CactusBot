"""Run CactusBot."""

from asyncio import get_event_loop

from coloredlogs import install

from config import SERVICE, USERNAME, PASSWORD


# TODO: move to Cactus
async def run():
    await SERVICE.run(USERNAME, PASSWORD)

install(level="DEBUG")

loop = get_event_loop()
try:
    loop.run_until_complete(run())
    loop.run_forever()
finally:
    loop.close()
