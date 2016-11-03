"""Uptime command."""

import re
from datetime import datetime

from . import Command

from ...packets import MessagePacket

import aiohttp

class Uptime(Command):
    """Uptime command."""

    @Command.subcommand()
    async def get(self, *args: False, channel: "channel"):
        data = await (await aiohttp.get(
            "https://beam.pro/api/v1/channels/160788/manifest.light2".format(channel)
        )).json()
        
        if data.get("startedAt") is not None:
            return "Channel has been live for {}.".format(
                re.match(
                    r"(.+)\.\d{6}",
                    str(datetime.utcnow() - datetime.strptime(
                        data["startedAt"][:-5], "%Y-%m-%dT%H:%M:%S"))
                ).group(1))

        return "Channel is offline."

    DEFAULT = get