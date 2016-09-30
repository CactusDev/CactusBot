"""Handle commands."""

from ..handler import Handler

import logging

from ..api import CactusAPI


class CommandHandler(Handler):
    """Command handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_message(self, packet):
        user = ""  # TODO: Implement internal packet format for transferring data
        message = ""  # TODO: Implement internal packet format for transferring data

        self.logger.info("[%s] %s", user, packet)

        if message.startswith('!') and len(message) > 1:
            command, *args = message.split()

