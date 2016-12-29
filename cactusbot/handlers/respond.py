"""Handle bot responses."""

from ..handler import Handler


class ResponseHandler(Handler):
    """Handle bot responses."""

    def __init__(self, username):
        super().__init__()

        self.username = username

    async def on_message(self, packet):
        """Handler message events."""

        if packet.user.lower() == self.username.lower():
            return StopIteration
