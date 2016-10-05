"""Handle incoming spam messages."""

from ..handler import Handler

import logging


class SpamHandler(Handler):
    """Spam handler."""

    MAX_SCORE = 16
    MAX_EMOTES = 6
    ALLOW_LINKS = False

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def on_message(self, packet):
        """Handle message events."""

        exceeds_caps = self.check_caps(''.join(
            chunk["text"] for chunk in packet if
            chunk["type"] == chunk["text"]
        ))
        contains_emotes = self.check_emotes(packet)
        has_links = self.check_links(packet)

        # FIXME: Make this return something that matters and is usable
        if exceeds_caps or contains_emotes or has_links:
            return True
        else:
            return False

    def check_links(self, packet):
        """Check for links in the message."""
        return not self.ALLOW_LINKS and any(
            chunk["type"] == "link" for chunk in packet)

    def check_emotes(self, packet):
        """Check for excessive emotes in the message."""
        return sum(chunk["type"] == "emote" for
                   chunk in packet) > self.MAX_EMOTES

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.MAX_SCORE
