"""Handle commands."""

import asyncio

from ..api import CactusAPI
from ..commands import COMMANDS
from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    def __init__(self, channel):
        super().__init__()

        self.channel = channel
        self.api = CactusAPI(channel)

        self.magics = dict((command.COMMAND, command(self.api))
                           for command in COMMANDS)

    async def on_message(self, packet):
        """Handle message events."""

        if len(packet) > 1 and packet[0] == "!" and packet[1] != ' ':
            command, *args = packet[1:].split()
            if command in self.magics:
                response = await self.magics[command](
                    *args, username=packet.user, channel=self.channel)
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

        if "%ARGS%" in packet and len(args) < 2:
            return MessagePacket("Not enough arguments!")

        packet.replace(**{
            "%ARGS%": ' '.join(args[1:]),
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return packet
