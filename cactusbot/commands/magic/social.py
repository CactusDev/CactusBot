"""Get social data."""

from . import Command
from ...packets import MessagePacket


class Social(Command):
    """Get social data."""

    COMMAND = "social"

    @Command.command(hidden=True)
    async def default(self, *services: False):
        """Get a social service if it's provived, or give it all."""

        if len(services) >= 12:
            return "Maximum number of requested services (12) exceeded."

        response = []
        if services:
            for service in services:
                social = await self.api.get_social(service)
                if social.status == 200:
                    data = await social.json()
                    response.append(
                        data["data"]["attributes"]["service"].title() + ': ')
                    response.append(
                        ("url", data["data"]["attributes"]["url"]))
                    response.append(', ')
                else:
                    return "'{}' not found on the streamer's profile!".format(
                        service)

            return MessagePacket(*response[:-1])
        else:
            social = await self.api.get_social()
            if social.status == 200:
                data = await social.json()

                for service in data["data"]:
                    response.append(
                        service["attributes"]["service"].title() + ': ')
                    response.append(("url", service["attributes"]["url"]))
                    response.append(', ')
                return MessagePacket(*response[:-1])
            else:
                return "'{}' not found on the streamer's profile!".format(
                    service)

    @Command.command()
    async def add(self, service, url):
        """Add a social service."""

        response = await self.api.add_social(service, url)
        if response.status == 201:
            return "Added social service {}.".format(service)
        elif response.status == 200:
            return "Updated social service {}".format(service)

    @Command.command()
    async def remove(self, service):
        """Remove a social service."""

        response = await self.api.remove_social(service)
        if response.status == 200:
            return "Removed social service {}.".format(service)
        elif response.status == 404:
            return "Social service {} doesn't exist!".format(service)
