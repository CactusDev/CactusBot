"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket

class EventHandler(Handler):
    """Events handler."""

    def on_subscribe(self, username):
        """Handle subscription packets."""
        return MessagePacket(
            ("text", "Thanks for subscribing, @{} !".format(username)),
            user="BOT USER"
        )

    def on_follow(self, username):
        """Handle follow packets."""
        return MessagePacket(
            ("text", "Thanks for following the channel, @{} !".format(username)),
            user="BOT USER"
        )

    def on_host(self, username):
        """Handle host packets."""
        return MessagePacket(
            ("text", "Thanks for hosting the channel, @{} !".format(username)),
            user="BOT USER"
        )
