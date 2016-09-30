"""Handle logging"""

from ..handler import Handler

import logging

class LoggingHandler(Handler):
    """Logging handler."""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def on_log(self, packet):
        """Handle logging events."""
        self.logger.info(''.join(chunk["text"] for chunk in packet))
        self.logger.debug(packet)
    
    def on_message(self, packet):
        """Handle message events."""
        self.logger.info(''.join(chunk["text"] for chunk in packet))
        self.logger.debug(packet)
