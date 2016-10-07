"""Handle commands."""

from ..handler import Handler


class CommandHandler(Handler):
    """Command handler."""

    BUILTINS = {
        "cactus": "Ohai! I'm CactusBot. :cactus",
        "test": "Test confirmed. :cactus",
        "help": "Check out my documentation at cactusbot.rtfd.org."
    }

    def on_message(self, packet):
        """Handle message events."""

        if packet[0] == "!" and len(packet) > 1:
            command, *args = packet[1:].split()
            if command in self.BUILTINS:
                self.logger.debug("args: %s", args)
                return self.BUILTINS[command]
            else:
                # TODO: Custom command stuff
                pass
