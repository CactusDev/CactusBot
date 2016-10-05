"""Handle logging."""

from ..handler import Handler


class LoggingHandler(Handler):
    """Logging handler."""

    def __init__(self):
        super().__init__()

    def on_message(self, packet):
        """Handle message events."""
        self.logger.info(packet["user"])
        # self.logger.info(
        #     packet["user_name"] + " - " +
        #     ''.join(chunk["text"] for chunk in packet["message"])
        # )

    def on_follow(self, packet):
        """Handle follow events."""
        self.logger.debug(packet)
        self.logger.info("- %s followed", packet["user"])

    def on_subscribe(self, packet):
        """Handle subscription events."""
        self.logger.debug(packet)
        self.logger.info("- %s subscribed", packet["user"])

    def on_resubscribe(self, packet):
        """Handle resubscription events."""
        self.logger.debug(packet)
        self.logger.info("- %s resbscribed", packet["user"])

    def on_host(self, packet):
        """Handle host events."""
        self.logger.debug(packet)
        self.logger.info("- %s hosted", packet["user"])

    def on_join(self, packet):
        """Handle user join events."""
        self.logger.debug(packet)
        self.logger.info("- %s joined", packet["user"])
