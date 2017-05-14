#!/usr/bin/env python3

"""Run CactusBot."""

import asyncio
import logging
from argparse import ArgumentParser

from cactusbot.cactus import CactusBot
from config import SEPAL_URL, SERVICE, api

async def run():
    """Run bot instance."""
    async with CactusBot(api, SERVICE, SEPAL_URL) as bot:
        await bot.run()

if __name__ == "__main__":

    parser = ArgumentParser(description="Run CactusBot.")

    parser.add_argument(
        "--debug",
        help="set custom logger level",
        metavar="LEVEL",
        nargs='?',
        const="DEBUG",
        default="INFO"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.debug,
        format="{asctime} {levelname} {name} {funcName}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style='{'
    )

    loop = asyncio.get_event_loop()

    tasks = asyncio.gather(
        asyncio.ensure_future(run())
    )

    try:
        loop.run_until_complete(tasks)

    except KeyboardInterrupt:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.run_forever()
        tasks.exception()

        print("Removing spines...")

    finally:
        loop.stop()
        loop.close()
