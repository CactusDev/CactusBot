"""Handle logging."""

from ..handler import Handler


class LoggingHandler(Handler):
    """Logging handler."""

    def on_message(self, packet):
        """Handle message events."""
        self.logger.debug(packet)
        self.logger.info(
            ''.join(chunk["text"] for chunk in packet if chunk["type"] == chunk["text"])
        )

    def on_follow(self, packet):
        """Handle follow events."""
        self.logger.debug(packet)
        # TODO: Info logging of the user that followed

    def on_subscribe(self, packet):
        """Handle subscription events."""
        self.logger.debug(packet)
        # TODO: Info logging of the user that subbed

    def on_resubscribe(self, packet):
        """Handle resubscription events."""
        self.logger.debug(packet)
        # TODO: Info logging of the user that resubbed
