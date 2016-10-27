"""Handle commands."""

import asyncio

from ..handler import Handler
from ..packets import MessagePacket
from ..commands import COMMANDS
from ..api import CactusAPI


class CommandHandler(Handler):
    """Command handler."""

    def __init__(self, channel):
        super().__init__()

        self.channel = channel
        self.api = CactusAPI(channel)
        self.loop = asyncio.new_event_loop()  # HACK

        self.MAGICS = dict((command.COMMAND, command(self.api))
                           for command in COMMANDS)

    def on_message(self, packet):
        """Handle message events."""

        if len(packet) > 1 and packet[0] == "!" and packet[1] != ' ':
            command, *args = packet[1:].split()
            if command in self.MAGICS:
                response = self.loop.run_until_complete(
                    self.MAGICS[command](
                        *args,
                        username=packet.user,
                        channel=self.channel
                    )
                )  # HACK: until asynchronous generators
                if packet.target:
                    response.target = packet.user
                return response
            else:
                # TODO: custom commands
                return self.inject(MessagePacket(args[0]), *args[1:])  # XXX

    @staticmethod
    def inject(packet, *args, **data):
        """Inject targets into a packet."""

        try:
            packet.sub(
                r'%ARG(\d+)%',
                lambda match: args[int(match.group(1))]
            )
        except IndexError:
            return MessagePacket("Not enough arguments!")

        packet.replace(**{
            "%ARGS%": ' '.join(args),
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return packet
