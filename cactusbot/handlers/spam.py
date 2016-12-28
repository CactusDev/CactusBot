"""Handle incoming spam messages."""

from ..handler import Handler
from ..packets import BanPacket, MessagePacket


class SpamHandler(Handler):
    """Spam handler."""

    def __init__(self):
        super().__init__()

        self.config = {
            "max_score": 16,
            "max_emoji": 6,
            "allow_urls": False
        }

    async def on_message(self, packet):
        """Handle message events."""

        if packet.role >= 50:  # FIXME: Replace with actual value
            return None

        exceeds_caps = self.check_caps(''.join(
            chunk.text for chunk in packet if
            chunk.type == "text"
        ))
        exceeds_emoji = self.check_emoji(packet)
        contains_urls = self.contains_urls(packet)

        if exceeds_caps:
            return (MessagePacket("Please do not spam capital letters.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)
        elif exceeds_emoji:
            return (MessagePacket("Please do not spam emoji.",
                                  target=packet.user),
                    BanPacket(packet.user, 1),
                    StopIteration)
        elif contains_urls:
            return (MessagePacket("Please do not post URLs.",
                                  target=packet.user),
                    BanPacket(packet.user, 5),
                    StopIteration)
        else:
            return None

    async def on_config(self, packet):
        """Handle config update events."""

        if packet.kwargs["key"] == "spam":
            self.config["max_emoji"] = packet.kwargs["values"]["maxEmoji"]
            self.config["max_score"] = packet.kwargs["values"]["maxCapsScore"]
            self.config["allow_urls"] = packet.kwargs["values"]["allowLinks"]

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.config["max_score"]

    def check_emoji(self, packet):
        """Check for excessive emoji in the message."""
        return sum(chunk.type == "emoji" for
                   chunk in packet) > self.config["max_emoji"]

    def contains_urls(self, packet):
        """Check for URLs in the message."""
        return not self.config["allow_urls"] and any(
            chunk.type == "link" for chunk in packet)
