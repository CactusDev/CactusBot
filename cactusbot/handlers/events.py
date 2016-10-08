"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket


class EventHandler(Handler):
    """Events handler."""

    def on_subscribe(self, packet):
        """Handle subscription packets."""
        return MessagePacket(
            ("text", "Thanks for subscribing, @{} !".format(packet.json["user"])),
            user="BOT USER"
        )

    def on_follow(self, packet):
        """Handle follow packets."""
        return MessagePacket(
            ("text", "Thanks for following the channel, @{} !".format(
                packet.json["user"])),
            user="BOT USER"
        )

    def on_host(self, packet):
        """Handle host packets."""
        return MessagePacket(
            ("text", "Thanks for hosting the channel, @{} !".format(packet.json["user"])),
            user="BOT USER"
        )
