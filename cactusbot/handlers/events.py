"""Handle events"""

import datetime

from ..cached import CacheUtils
from ..handler import Handler
from ..packets import MessagePacket

from ..api import CactusAPI


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_data, channel):
        super().__init__()

        self.cache = CacheUtils("caches/followers.json")
        self.cache_follows = cache_data["CACHE_FOLLOWS"]
        self.follow_time = datetime.timedelta(
            minutes=cache_data["CACHE_FOLLOWS_TIME"])

        self.api = CactusAPI(channel)

        self.alert_messages = None

    async def load_messages(self):
        """Load alert messages."""

        data = self.api.get_config()

        if not data.get("data"):
            return

        if not data["data"].get("announce"):
            return

        messages = data["data"]["announce"]

        self.alert_messages = {
            "follow": messages["follow"],
            "subscribe": messages["sub"],
            "host": messages["host"]
        }

    async def on_start(self, _):
        """Handle start packets."""

        return MessagePacket(
            "CactusBot activated. ",
            ("emoji", ":cactus:", ":cactus:")
        )

    async def on_follow(self, packet):
        """Handle follow packets."""

        if not self.alert_messages["follow"]["announce"]:
            return

        response = MessagePacket.from_json(
            self.alert_messages["follow"]["message"].replace("%USER%", packet.user))

        if packet.success:
            if self.cache_follows:
                now = datetime.datetime.utcnow()
                if packet.user in self.cache:
                    cache_time = self.cache[packet.user]
                    if cache_time + self.follow_time <= now:
                        self.cache[packet.user] = now.isoformat()
                        return response
                else:
                    self.cache[packet.user] = now.isoformat()
                    return response
            else:
                return response

    async def on_subscribe(self, packet):
        """Handle subscription packets."""

        if not self.alert_messages["subscribe"]["announce"]:
            return

        return MessagePacket.from_json(
            self.alert_messages["subscribe"]["message"].replace("%USER%", packet.user))

    async def on_host(self, packet):
        """Handle host packets."""

        if not self.alert_messages["host"]["announce"]:
            return

        return MessagePacket.from_json(
            self.alert_messages["host"]["message"].replace("%USER%", packet.user))

    async def on_config(self, packet):
        """Handle config update events."""

        messages = packet["data"]["announce"]

        self.alert_messages = {
            "follow": messages["follow"],
            "subscribe": messages["sub"],
            "host": messages["host"]
        }
