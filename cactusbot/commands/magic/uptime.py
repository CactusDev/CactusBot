"""Uptime command."""

import re
from datetime import datetime

from . import Command

import aiohttp


class Uptime(Command):
    """Uptime command."""

    @Command.subcommand
    async def get(self, *, channel: "channel"):
        data = await (await aiohttp.get(
            "https://beam.pro/api/v1/channels/{channel}/manifest.light2".format(
                channel=channel))).json()

        if "startedAt" in data:
            time = datetime.utcnow() - datetime.strptime(
                        data["startedAt"], "%Y-%m-%dT%H:%M:%S.%f")
            time -= datetime.timedelta(microseconds=time.microseconds)
            return "Channel has been live for {}.".format(time)

        return "Channel is offline."

    DEFAULT = get
