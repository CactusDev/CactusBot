"""Handle commands."""

from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    BUILTINS = {
        "cactus": MessagePacket(
            ("text", "Ohai! I'm CactusBot. "),
            ("emoticon", "cactus", ":cactus"),
            user="BOT USER"
        ),
        "test": MessagePacket(
            ("text", "Test confirmed. "),
            ("emoticon", "cactus", ":cactus"),
            user="BOT USER"
        ),
        "help": MessagePacket(
            ("text", "Check out my documentation at "),
            ("link", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
            ("text", "."),
            user="BOT USER"
        )
    }

    def on_message(self, packet):
        """Handle message events."""

        if packet[0] == "!" and len(packet) > 1:
            command, *args = packet[1:].split()
            if command in self.BUILTINS:
                return self.BUILTINS[command]
            else:
                # TODO: Custom command responses from the API
                pass
