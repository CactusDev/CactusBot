"""Handle logging."""

from ..handler import Handler


class LoggingHandler(Handler):
    """Logging handler."""

    def on_message(self, packet):
        """Handle message events."""
        self.logger.info("%s: %s", packet.user, packet.text)

    def on_join(self, packet):
        """Handle user join events."""
        self.logger.info("%s joined", packet)

    def on_leave(self, packet):
        """Handle user join events."""
        self.logger.info("%s left", packet)

    def on_follow(self, packet):
        """Handle follow events."""
        self.logger.info("%s followed", packet)

    def on_subscribe(self, packet):
        """Handle subscription events."""
        self.logger.info("%s subscribed", packet)

    def on_resubscribe(self, packet):
        """Handle resubscription events."""
        self.logger.info("%s resubscribed", packet)

    def on_host(self, packet):
        """Handle host events."""
        self.logger.info("%s hosted", packet)
