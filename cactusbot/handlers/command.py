"""Handle commands."""

import asyncio
import re

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
                    self.MAGICS[command](*args, channel=self.channel)
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

        try:
            # FIXME: Packet text isn't containing anything after a space.
            # This regex should be changed to '%ARG(\d+|S)(?:=([^ ]+))?(?: \| (\w+))?%'
            # When this is fixed
            match = re.match(
                r'%ARG(\d+|S)(?:=([^ ]+))?(?:\|(\w+))?%', packet.text)
        except AttributeError:
            pass

        if match is not None and len(match.groups()) == 3:
            match = match.groups()

            if match[0] == "S":
                if match[2].lower() == "upper":
                    args = ' '.join(
                        arg.upper() for arg in args
                    )
                elif match[2].lower() == "lower":
                    args = ' '.join(
                        arg.lower() for arg in args
                    )
                elif match[2].lower() == "title":
                    args = ' '.join(args).title()
                packet.replace(**{"|{}".format(match[2]): ''})
            else:
                try:
                    int(match[0])
                except ValueError:
                    return
                else:
                    arg = int(match[0])
                    if arg > len(args):
                        return MessagePacket("Not enough arguments!")
                    args = args[arg]

                    if match[2].lower() == "upper":
                        args = args.upper()
                    elif match[2].lower() == "lower":
                        args = args.lower()
                    elif match[2].lower() == "title":
                        args = args.title()

                    packet.replace(**{"|{}".format(match[2]): ''})
                    packet.replace(**{"%ARG{}%".format(arg): args})
        else:
            args = ' '.join(args)

        packet.replace(**{
            "%ARGS%": args,
            "%USER%": data.get("username"),
            "%COUNT%": "%COUNT%",  # TODO
            "%CHANNEL%": data.get("channel")
        })

        return packet
