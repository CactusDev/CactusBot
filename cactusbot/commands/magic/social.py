"""Get social data."""

from . import Command
from ...packets import MessagePacket


@Command.command()
class Social(Command):
    """Get social data."""

    COMMAND = "social"

    @Command.command(hidden=True)
    async def default(self, *services: False):
        """Get a social service if it's provived, or give it all."""

        response = []
        if services:
            for service in services:
                social = await self.api.get_social(service)
                if social.status == 200:
                    data = await social.json()
                    response.append(data["data"]["attributes"]["service"].title() + ': ')
                    response.append(("url", data["data"]["attributes"]["url"]))
                    response.append(', ')
                else:
                    return "'{services}' not found on the streamer's profile!".format(
                        s='s' if len(services) > 1 else '', services=', '.join(services))
            return MessagePacket(*response[:-1])
        else:
            social = await self.api.get_social()
            if social.status == 200:
                data = await social.json()

                for service in data["data"]:
                    print(service)
                    response.append(service["attributes"]["service"].title() + ': ')
                    response.append(("url", service["attributes"]["url"]))
                    response.append(', ')
                return MessagePacket(*response[:-1])
            else:
                return "'{services}' not found on the streamer's profile!".format(
                    services=', '.join(services))

    @Command.command()
    async def add(self, service, url):
        """Add a social service."""

        response = self.api.add_social(service, url)
        if response.status == 201:
            return "Added social service {}.".format(service)
        elif response.status == 200:
            return "Updated social service {}".format(service)

    @Command.command()
    async def remove(self, service):
        """Remove a social service."""

        response = self.api.remove_social(service)
        if response.status == 200:
            return "Removed social service {}.".format(service)
        elif response.status == 404:
            return "Social service {} doesn't exist!".format(service)
