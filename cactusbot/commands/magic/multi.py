"""Generate a multistream link."""

from . import Command
from ...packets import MessagePacket

_BASE_URL = "https://multistream.me/"
_SERVICES = ['t', 'b', 'h', 'y']


class Multi(Command):
    """Generate a multistream link."""

    COMMAND = "multi"

    @Command.command(hidden=True)
    async def default(self, *channels):
        """Create a multistream link using a list of channels, and services
        seperated by `:`.

        !multistream b:fun h:streamer t:to y:watch
        """

        link = _BASE_URL

        for channel in channels:
            service, channel_name = channel.split(':')

            if service not in _SERVICES:
                return "'{}' is not a valid service.".format(service)

            link += "{service}:{channel}/".format(
                service=service, channel=channel_name)

        return MessagePacket(("url", link))
