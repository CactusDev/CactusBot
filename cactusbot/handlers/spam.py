"""Handle incoming spam messages."""

from ..handler import Handler
from ..packets import BanPacket


class SpamHandler(Handler):
    """Spam handler."""

    MAX_SCORE = 16
    MAX_EMOTES = 6
    ALLOW_LINKS = False

    def on_message(self, packet):
        """Handle message events."""

        if packet.role >= 50:  # FIXME: Replace with actual value
            return None

        exceeds_caps = self.check_caps(''.join(
            chunk["text"] for chunk in packet if
            chunk["type"] == "text"
        ))
        contains_emotes = self.check_emotes(packet)
        has_links = self.check_links(packet)

        if exceeds_caps:
            return BanPacket(packet.user, 1)
        elif contains_emotes:
            return BanPacket(packet.user, 25)
        elif has_links:
            return BanPacket(packet.user, 5)
        else:
            return None

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.MAX_SCORE

    def check_emotes(self, packet):
        """Check for excessive emotes in the message."""
        return sum(chunk["type"] == "emoticon" for
                   chunk in packet) > self.MAX_EMOTES

    def check_links(self, packet):
        """Check for links in the message."""
        return not self.ALLOW_LINKS and any(
            chunk["type"] == "link" for chunk in packet)
