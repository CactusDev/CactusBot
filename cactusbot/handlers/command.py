"""Handle commands."""

import asyncio

from ..api import CactusAPI
from ..commands import COMMANDS
from ..handler import Handler
from ..packets import MessagePacket


class CommandHandler(Handler):
    """Command handler."""

    ARGN_EXPR = r'%ARG(\d+)(?:=([^|]+))?(?:((?:\|\w+)+))?%'
    ARGS_EXPR = r'%ARGS(?:=([^|]+))?(?:((?:\|\w+)+))?%'
    MODIFIERS = {
        "upper": str.upper,
        "lower": str.lower,
        "title": str.title,
        "reverse": lambda text: text[::-1],
        "tag": lambda tag: tag[1:] if tag[0] == '@' and len(tag) > 1 else tag
    }

    def __init__(self, channel):
        super().__init__()

        self.channel = channel
        self.api = CactusAPI(channel)
        self.loop = asyncio.new_event_loop()  # HACK

        self.magics = dict((command.COMMAND, command(self.api))
                           for command in COMMANDS)

    def on_message(self, packet):
        """Handle message events."""

        if len(packet) > 1 and packet[0] == "!" and packet[1] != ' ':
            command, *args = packet[1:].split()
            if command in self.magics:
                response = self.loop.run_until_complete(
                    self.magics[command](*args, channel=self.channel)
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
            """Substitute an argument in place of an ARGN target."""

            argn, default, modifiers = match.groups()
            argn = int(argn)

            if default is None:
                result = args[argn]
            else:
                result = args[argn] if argn < len(args) else default

            if modifiers is not None:
                result = self.modify(result, *modifiers.split('|')[1:])

            return result

        try:
            packet.sub(self.ARGN_EXPR, sub_argn)
        except IndexError:
            return "Not enough arguments!"

        def sub_args(match):
            """Substitute all arguments in place of the ARGS target."""

            default, modifiers = match.groups()

            if not args[1:] and default is not None:
                result = default
            else:
                result = ' '.join(args[1:])

            if modifiers is not None:
                result = self.modify(result, *modifiers.split('|')[1:])

            return result

        packet.sub(self.ARGS_EXPR, sub_args)

        packet.replace(**{
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return packet

    def modify(self, argument, *modifiers):
        """Apply modifiers to an argument."""

        for modifier in modifiers:
            if modifier in self.MODIFIERS:
                argument = self.MODIFIERS[modifier](argument)

        return argument
