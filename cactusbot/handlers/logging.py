"""Handle logging"""

from ..handler import Handler

import logging

class LoggingHandler(Handler):
    """Logging handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_log(self, packet):
        """Handle logging events."""
        # XXX: This is subject to change. We'll have to see what the data structure ends up as.
        self.logger.info(packet["message"])
        self.logger.debug(packet)
