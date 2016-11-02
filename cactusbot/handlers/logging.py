"""Handle logging."""

from ..handler import Handler


class LoggingHandler(Handler):
    """Logging handler."""

    async def on_message(self, packet):
        """Handle message events."""
        self.logger.info("%s: %s", packet.user, packet.text)

    async def on_join(self, packet):
        """Handle user join events."""
        self.logger.info("%s joined", packet.user)

    async def on_leave(self, packet):
        """Handle user join events."""
        self.logger.info("%s left", packet.user)

    async def on_follow(self, packet):
        """Handle follow events."""
        self.logger.info("%s followed", packet.user)

    async def on_subscribe(self, packet):
        """Handle subscription events."""
        self.logger.info("%s subscribed", packet.user)

    async def on_resubscribe(self, packet):
        """Handle resubscription events."""
        self.logger.info("%s resubscribed", packet.user)

    async def on_host(self, packet):
        """Handle host events."""
        self.logger.info("%s hosted", packet.user)
