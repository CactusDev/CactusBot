"""Handle commands."""

from ..handler import Handler

import logging

from ..api import CactusAPI


class CommandHandler(Handler):
    """Command handler."""

    def on_message(self, packet):
        """Handle message events."""
        user = ""  # TODO: Implement internal packet format for transferring data
        message = ""  # TODO: Implement internal packet format for transferring data

        self.log(packet)

        if message.startswith('!') and len(message) > 1:
            command, *args = message.split()
