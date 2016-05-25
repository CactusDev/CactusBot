from coloredlogs import install

from config import SERVICE, USERNAME, PASSWORD
from asyncio import get_event_loop


async def run():
    async with SERVICE as beam:
        # TODO: move to internals of BeamChat
        login_data = await beam.login(USERNAME, PASSWORD)
        beam.chat = await beam.get_chat(beam.channel_data["id"])
        await beam._authenticate(
            beam.channel_data["id"], login_data["id"], beam.chat["authkey"])
        await beam.read()

install(level="DEBUG")

get_event_loop().run_until_complete(run())
