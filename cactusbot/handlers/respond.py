"""Handle bot responses."""

from ..handler import Handler


class ResponseHandler(Handler):
    """Handle bot responses."""

    def __init__(self):
        super().__init__()

        self.username = ""

    async def on_username_update(self, packet):
        """Set the username of the bot."""
        print(packet.json)
        self.username = packet.json["username"]

    async def on_message(self, packet):
        """Handler message events."""

        if packet.user.lower() == self.username.lower():
            return StopIteration
