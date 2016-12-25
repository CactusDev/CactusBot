"""Uptime command."""

import datetime

import aiohttp

from . import Command


@Command.command()
class Uptime(Command):
    """Uptime command."""

    BEAM_MANIFEST_URL = ("https://beam.pro/api/v1/channels/{channel}"
                         "/manifest.light2")

    @Command.command(hidden=True)
    async def default(self, *, channel: "channel"):
        """Default response."""

        data = await (await aiohttp.get(
            self.BEAM_MANIFEST_URL.format(channel=channel)
        )).json()

        if "startedAt" in data:
            time = datetime.datetime.utcnow() - datetime.datetime.strptime(
                data["startedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            time -= datetime.timedelta(microseconds=time.microseconds)
            return "Channel has been live for {}.".format(time)

        return "Channel is offline."
