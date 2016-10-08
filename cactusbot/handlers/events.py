"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket


class EventHandler(Handler):
    """Events handler."""

    def on_follow(self, packet):
        """Handle follow packets."""
        if packet.success:
            return MessagePacket(
                # TODO: Make configurable
                ("text", "Thanks for following, @{} !".format(packet.user)),
                user="BOT USER"
            )

    def on_subscribe(self, packet):
        """Handle subscription packets."""
        return MessagePacket(
            # TODO: Make configurable
            ("text", "Thanks for subscribing, @{} !".format(packet.user)),
            user="BOT USER"
        )

    def on_host(self, packet):
        """Handle host packets."""
        return MessagePacket(
            # TODO: Make configurable
            ("text", "Thanks for hosting, @{} !".format(packet.user)),
            user="BOT USER"
        )
