"""Run CactusBot."""

from asyncio import get_event_loop

from cactusbot import Cactus

from config import SERVICE, USERNAME, PASSWORD


if __name__ == "__main__":

    loop = get_event_loop()

    cactus = Cactus(SERVICE)

    try:
        loop.run_until_complete(cactus.run(USERNAME, PASSWORD))
        loop.run_forever()
    finally:
        loop.close()
