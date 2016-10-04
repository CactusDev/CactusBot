"""Handle commands."""

from ..handler import Handler


class CommandHandler(Handler):
    """Command handler."""

    BUILTINS = {
        "cactus": "Ohai! I'm CactusBot. :cactus",
        "test": "Test confirmed :cactus",
        "help": "Check out my documentation at cactusbot.rtfd.org"
    }

    def on_message(self, packet):
        """Handle message events."""

        message = ''.join(chunk["text"] for chunk in packet if chunk["type"] == chunk["text"])

        if message.startswith('!') and len(message) > 1:
            command, *args = message.split()
            if command in self.BUILTINS:
                # TODO: Make this send the response of that command.
                pass
            else:
                # TODO: Poll the api and see if the command exists.
