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

        message = ''.join(chunk["text"] for chunk in packet["message"])
        if message[0] == "!":
            command = message[1:]
            if command in self.BUILTINS:
                print(self.BUILTINS[command])
            else:
                # TODO: Custom command stuff
                pass
