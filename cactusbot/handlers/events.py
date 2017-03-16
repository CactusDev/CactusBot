"""Handle events"""

import time

from ..handler import Handler
from ..packets import MessagePacket


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_data, api):
        super().__init__()

        self.cache_data = cache_data
        self.cached_events = {}

        self.api = api

        self.cached_events = {
            "follow": {},
            "join": {},
            "leave": {},
            "host": {}
        }

        self.alert_messages = {
            "follow": {
                "announce": True,
                "message": "Thanks for following, %USER%!"
            },
            "subscribe": {
                "announce": True,
                "message": "Thanks for subscribing, %USER%!"
            },
            "host": {
                "announce": True,
                "message": "Thanks for hosting, %USER%!"
            },
            "join": {
                "announce": False,
                "message": "Welcome to the channel, %USER%!"
            },
            "leave": {
                "announce": False,
                "message": "Thanks for watching, %USER%!"
            }
        }

    async def load_messages(self):
        """Load alert messages."""

        data = await (await self.api.get_config()).json()

        messages = data["data"]["attributes"]["announce"]

        self.alert_messages = {
            "follow": messages["follow"],
            "subscribe": messages["sub"],
            "host": messages["host"],
            "join": messages["join"],
            "leave": messages["leave"]
        }

    async def on_start(self, _):
        """Handle start packets."""

        await self.load_messages()

        return MessagePacket("CactusBot activated. ", ("emoji", "🌵"))

    async def on_follow(self, packet):
        """Handle follow packets."""

        if not self.alert_messages["follow"]["announce"]:
            return

        return await self._cache(packet, "follow")

    async def on_subscribe(self, packet):
        """Handle subscription packets."""

        if self.alert_messages["subscribe"]["announce"]:
            return MessagePacket(
                self.alert_messages["subscribe"]["message"].replace(
                    "%USER%", packet.user
                ))

    async def on_host(self, packet):
        """Handle host packets."""

        if not self.alert_messages["host"]["announce"]:
            return

        return await self._cache(packet, "host")

    async def on_join(self, packet):
        """Handle join packets."""

        if not self.alert_messages["join"]["announce"]:
            return

        return await self._cache(packet, "join")

    async def on_leave(self, packet):
        """Handle leave packets."""

        if not self.alert_messages["leave"]["announce"]:
            return

        return await self._cache(packet, "leave")

    async def on_config(self, packet):
        """Handle config update events."""

        values = packet.kwargs["values"]
        if packet.kwargs["key"] == "announce":
            self.alert_messages = {
                "follow": values["follow"],
                "subscribe": values["sub"],
                "host": values["host"],
                "join": values["join"],
                "leave": values["leave"]
            }

    async def _cache(self, packet, event):
        if hasattr(packet, "user"):
            response = MessagePacket(
                self.alert_messages[event]["message"].replace(
                    "%USER%", packet.user
                ))
        else:
            return None

        if packet.success:
            if self.cache_data["cache_{}".format(event)]:
                user = packet.user
                if user in self.cached_events[event]:
                    since = time.time() - self.cached_events[event][user]
                    if since >= self.cache_data["cache_time"]:
                        self.cached_events[event][user] = time.time()
                        return response
                else:
                    self.cached_events[event][user] = time.time()
                    return response
            else:
                return response
        return None
