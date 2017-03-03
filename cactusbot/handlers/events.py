"""Handle events"""

import time

from ..handler import Handler
from ..packets import MessagePacket


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_data, api):
        super().__init__()

        self.cache_follows = cache_data["CACHE_FOLLOWS"]
        self.cache_hosts = cache_data["CACHE_HOSTS"]
        self.cache_joins = cache_data["CACHE_JOINS"]
        self.cache_leaves = cache_data["CACHE_LEAVES"]
        self.cache_time = cache_data["CACHE_TIME"]

        self.cached_follows = {}
        self.cached_hosts = {}
        self.cached_joins = {}
        self.cached_leaves = {}

        self.api = api

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

        response = MessagePacket(
            self.alert_messages["follow"]["message"].replace(
                "%USER%", packet.user
            ))

        if packet.success:
            if self.cache_follows:
                if packet.user in self.cached_follows:
                    since_follow = time.time() - self.cached_follows[packet.user]
                    if since_follow >= self.cache_time:
                        self.cached_follows[packet.user] = time.time()
                        return response
                else:
                    self.cached_follows[packet.user] = time.time()
                    return response
            else:
                return response

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

        response = MessagePacket(
            self.alert_messages["host"]["message"].replace(
                "%USER%", packet.user
            ))

        if packet.success:
            if self.cache_hosts:
                if packet.user in self.cached_hosts:
                    since_host = time.time() - self.cached_hosts[packet.user]
                    if since_host >= self.cache_time:
                        self.cached_hosts[packet.user] = time.time()
                        return response
                else:
                    self.cached_hosts[packet.user] = time.time()
                    return response
            else:
                return response

    async def on_join(self, packet):
        """Handle join packets."""

        if not self.alert_messages["join"]["announce"]:
            return

        response = MessagePacket(
            self.alert_messages["join"]["message"].replace(
                "%USER%", packet.user
            ))

        if packet.success:
            if self.cache_joins:
                if packet.user in self.cached_joins:
                    since_join = time.time() - self.cached_joins[packet.user]
                    if since_join >= self.cache_time:
                        self.cached_joins[packet.user] = time.time()
                        return response
                else:
                    self.cached_joins[packet.user] = time.time()
                    return response
            else:
                return response

    async def on_leave(self, packet):
        """Handle leave packets."""

        if not self.alert_messages["leave"]["announce"]:
            return

        response = MessagePacket(
            self.alert_messages["leave"]["message"].replace(
                "%USER%", packet.user
            ))

        if packet.success:
            if self.cache_leaves:
                if packet.user in self.cached_leaves:
                    since_leave = time.time() - self.cached_leaves[packet.user]
                    if since_leave >= self.cache_time:
                        self.cached_leaves[packet.user] = time.time()
                        return response
                else:
                    self.cached_leaves[packet.user] = time.time()
                    return response
            else:
                return response

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
