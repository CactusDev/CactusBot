from logging import getLogger

from asyncio import ensure_future

# from .api import BeamAPI
from .chat import BeamChat
# from .liveloading import BeamLiveloading

from .. import Handler


class Beam(BeamChat, Handler):

    def __init__(self, channel, **kwargs):
        super().__init__(channel, **kwargs)

        self.logger = getLogger(__name__)

        self.channel = channel

        self.chat_events = {
            "ChatMessage": self.on_message,
            "UserJoin": self.on_join,
            "UserLeave": self.on_leave
        }

    async def __aenter__(self):
        await super().__aenter__()

        return self

    async def run(self, *auth):
        # TODO: insta-efficiency. just add logic!
        login_data = await self.login(*auth)
        self.chat = await self.get_chat(self.channel_data["id"])
        await self._authenticate(
            login_data["id"], self.chat["authkey"])
        await self.read(self.handle_chat)

    async def handle_chat(self, response):
        """Handle responses from a Beam websocket."""

        data = response.get("data")
        if data is None:
            return

        event = response.get("event")
        if event in self.chat_events:
            ensure_future(self.chat_events[event](data))
        elif response.get("id") is "auth":
            if data.get("authenticated") is True:
                await self.send("CactusBot activated. Enjoy! :cactus")
            else:
                self.logger.error("Chat authentication failure!")

    async def on_message(self, data):
        """Handle chat message packets from Beam."""

        parsed = ''.join([
            chunk["data"] if chunk["type"] == "text" else chunk["text"]
            for chunk in data["message"]["message"]
        ])

        await super().on_message(parsed, data["user_name"])

    async def on_join(self, data):
        """Handle user join packets from Beam."""
        await super().on_join(data["username"])

    async def on_leave(self, data):
        """Handle user leave packets from Beam."""
        await super().on_leave(data["username"])
