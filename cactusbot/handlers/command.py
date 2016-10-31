"""Handle commands."""

import asyncio
import re

from ..api import CactusAPI
from ..commands import COMMANDS
from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    ARGN_EXPR = r'%ARG(\d+)(?:=([^|]+))?(?:\|(\w+))?%'
    ARGS_EXPR = r'%ARGS(?:=([^|]+))?(?:\|(\w+))?%'
    FILTERS = {
        "upper": str.upper,
        "lower": str.lower
    }

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
                    self.MAGICS[command](*args, channel=self.channel)
                )  # HACK: until asynchronous generators
                if packet.target:
                    response.target = packet.user
                return response
            else:
                # TODO: custom commands
                return self.inject(MessagePacket(args[0]), *args[1:])  # XXX

    def inject(self, packet, *args, **data):
        """Inject targets into a packet."""

        def sub_argn(match):
            n, default, modifier = match.groups()
            n = int(n)

            if default is None:
                result = args[n]
            else:
                result = args[n] if n < len(args) else default

            if modifier is not None and modifier in self.FILTERS:
                result = self.FILTERS[modifier](result)

            return result

        try:
            packet.sub(self.ARGN_EXPR, sub_argn)
        except IndexError:
            return "Not enough arguments!"

        def sub_args(match):
            default, modifier = match.groups()

            if not args[1:] and default is not None:
                result = default
            else:
                result = ' '.join(args[1:])

            if modifier is not None and modifier in self.FILTERS:
                result = self.FILTERS[modifier](result)

            return result

        packet.sub(self.ARGS_EXPR, sub_args)

        packet.replace(**{
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return packet
