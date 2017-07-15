"""Uptime command."""

import datetime

import aiohttp

from . import Command


class Uptime(Command):
    """Uptime command."""

    COMMAND = "uptime"

    MIXER_MANIFEST_URL = ("https://mixer.com/api/v1/channels/{channel}"
                          "/manifest.light2")

    @Command.command(hidden=True)
    async def default(self, *, channel: "channel"):
        """Default response."""

        response = await (await aiohttp.get(
            "https://mixer.com/api/v1/channels/{}".format(channel)
        )).json()

        if "id" in response:
            data = await (await aiohttp.get(
                self.MIXER_MANIFEST_URL.format(channel=response["id"])
            )).json()

            if "startedAt" in data:
                time = datetime.datetime.utcnow() - datetime.datetime.strptime(
                    data["startedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                time -= datetime.timedelta(microseconds=time.microseconds)
                return "Channel has been live for {}.".format(time)

        return "Channel is offline."
