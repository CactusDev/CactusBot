"""Get social data."""

import json

from . import Command
from ...packets import MessagePacket

import aiohttp


class Social(Command):
    """Get social data."""

    COMMAND = "social"

    @Command.subcommand(hidden=True)
    async def get(self, *args: False, channel: "channel"):
        """Get a social service if it's provived, or give it all."""

        social_data = await (await aiohttp.get(
            "https://beam.pro/api/v1/channels/{}".format(channel)
        )).json()

        social_data = social_data["user"]["social"]

        if not social_data:
            return MessagePacket(
                (
                    "text",
                    "No social services found on this streamer's profile."
                ),
                user="BOT USER"
            )
        if not args:
            if "verified" in social_data:
                print("social")
                del social_data["verified"]
            return MessagePacket(
                ("text", ', '.join('{}: {}'.format(service.title(), url) for
                                   service, url in social_data.items())),
                user="BOT USER"
            )
        else:
            selected = set(map(str.lower, args))
            available = set(social_data.keys())

            if selected.issubset(available):
                return MessagePacket(
                    ("text", ', '.join('{}: {}'.format(
                        service.title(), social_data[service]
                        ) for service in selected)),
                    user="BOT USER"
                )
            return MessagePacket(
                ("text", "The service{s} {services} don't exist.".format(
                    services=', '.join(
                        selected.difference(available)), s='s' if len(
                            selected.difference(available) > 1) else '')),
                user="BOT USER"
            )

    DEFAULT = get
