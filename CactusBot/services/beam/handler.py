from logging import getLogger

from .. import Handler

from .api import BeamAPI
from .chat import BeamChat
from .liveloading import BeamLiveloading


class BeamHandler(Handler):

    def __init__(self, channel):
        super().__init__()

        self.logger = getLogger(__name__)

        self.api = BeamAPI()

        self._channel = channel

        # TODO: move here
        # self.chat = BeamChat(self.channel["id"], chat["endpoints"])

        self.chat_events = {
            "ChatMessage": self.on_message,
            "UserJoin": self.on_join,
            "UserLeave": self.on_leave
        }

    async def run(self, *auth):
        channel = await self.api.get_channel(self._channel)

        user = await self.api.login(*auth)
        chat = await self.api.get_chat(channel["id"])

        self.chat = BeamChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(user["id"], chat["authkey"])
        await self.chat.read(self.handle_chat)

    async def handle_chat(self, response):
        """Handle responses from a Beam websocket."""

        data = response.get("data")
        if data is None:
            return

        event = response.get("event")
        if event in self.chat_events:
            await self.chat_events[event](data)
        elif response.get("id") == "auth":
            if data.get("authenticated") is True:
                await self.chat.send("CactusBot activated. Enjoy! :cactus")
            else:
                self.logger.error("Chat authentication failure!")

    async def send(self, *args, **kwargs):
        if args is not None and args[0] is not None:  # TODO: fix
            await self.chat.send(*args, **kwargs)

    async def on_message(self, data):
        """Handle chat message packets from Beam."""

        parsed = ''.join([
            chunk["data"] if chunk["type"] == "text" else chunk["text"]
            for chunk in data["message"]["message"]
        ])

        await self.send(await super().on_message(parsed, data["user_name"]))

    async def on_join(self, data):
        """Handle user join packets from Beam."""
        await self.send(await super().on_join(data["username"]))

    async def on_leave(self, data):
        """Handle user leave packets from Beam."""
        await self.send(await super().on_leave(data["username"]))
