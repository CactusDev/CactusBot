"""Handle incoming spam messages."""

from ..handler import Handler

import logging

class SpamHandler(Handler):
    """Spam handler."""

    MAX_SCORE = 16
    MAX_EMOTES = 6
    ALLOW_LINKS = False

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_message(self, packet):
        """Handle message events."""
        built_message = ""
        for chunk in packet:
            if chunk["type"] == "text":
                built_message += chunk["text"]
        exceeds_caps = self.check_caps(built_message)
        contains_emotes = self.check_emotes(packet)
        has_links = self.check_links(packet)

        if exceeds_caps or contains_emotes or has_links:
            return True
        else:
            return False

    def check_links(self, packet):
        return not self.ALLOW_LINKS and any(chunk["type"] == "link" for chunk in packet)
        
    def check_emotes(self, packet):
        return sum(chunk["type"] == "emote" for chunk in packet) > self.MAX_EMOTES

    def check_caps(self, message):
        return sum(char.isupper() - char.islower() for char in message) > self.MAX_SCORE
