"""Handle incoming spam messages."""

import aiohttp

from ..handler import Handler
from ..packets import BanPacket, MessagePacket

BASE_URL = "https://beam.pro/api/v1/channels/{username}"


async def get_user_id(username):
    async with aiohttp.get(BASE_URL.format(username=username)) as response:
        if response.status == 404:
            return 0
        return (await response.json())["id"]


class SpamHandler(Handler):
    """Spam handler."""

    def __init__(self, api):
        super().__init__()

        self.api = api

        self.config = {
            "max_score": 16,
            "max_emoji": 6,
            "allow_urls": False,
            "whitelisted_urls": []
        }

    async def on_message(self, packet):
        """Handle message events."""

        if packet.role >= 4:
            return

        user_id = await get_user_id(packet.user)
        if (await self.api.get_trust(user_id)).status == 200:
            return

        exceeds_caps = self.check_caps(''.join(
            chunk.text for chunk in packet if
            chunk.type == "text"
        ))
        exceeds_emoji = self.check_emoji(packet)
        contains_urls = self.contains_urls(packet)

        if exceeds_caps:
            return (MessagePacket("Please do not spam capital letters.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)
        elif exceeds_emoji:
            return (MessagePacket("Please do not spam emoji.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)
        elif contains_urls:
            return (MessagePacket("Please do not post URLs.",
                                  target=packet.user),
                    BanPacket(packet.user, 5),
                    StopIteration)
        else:
            return None

    async def on_config(self, packet):
        """Handle config update events."""

        values = packet.kwargs["values"]
        if packet.kwargs["key"] == "spam":
            self.config["max_emoji"] = values["maxEmoji"]
            self.config["max_score"] = values["maxCapsScore"]
            self.config["allow_urls"] = values["allowUrls"]
            self.config["whitelisted_urls"] = values["whitelistedUrls"]

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.config["max_score"]

    def check_emoji(self, packet):
        """Check for excessive emoji in the message."""
        return sum(chunk.type == "emoji" for
                   chunk in packet) > self.config["max_emoji"]

    def contains_urls(self, packet):
        """Check for URLs in the message."""
        return not self.config["allow_urls"] and any(
            chunk.type == "url"
            and chunk.data not in self.config["whitelisted_urls"]
            for chunk in packet)
