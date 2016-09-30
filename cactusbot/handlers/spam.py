"""Handle incoming spam messages."""

from ..handler import Handler

import logging

class SpamHandler(Handler):
    """Spam handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_message(self, packet):
        """Handle message events."""
        user = ""
        message = ""

    def check_links(self, message):
        pass
        
    def check_emotes(self, message):
        pass

    def check_caps(self, message):
        pass
