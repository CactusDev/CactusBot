"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket


class EventHandler(Handler):
    """Events handler."""

    def on_follow(self, packet):
        """Handle follow packets."""
        if packet.success:
            # TODO: Make configurable
            return MessagePacket(
                "Thanks for following, @{} !".format(packet.user)
            )

    def on_subscribe(self, packet):
        """Handle subscription packets."""
        # TODO: Make configurable
        return MessagePacket(
            "Thanks for subscribing, @{} !".format(packet.user)
        )

    def on_host(self, packet):
        """Handle host packets."""
        # TODO: Make configurable
        return MessagePacket("Thanks for hosting, @{} !".format(packet.user))
