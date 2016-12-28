"""Trust command."""

from ..command import Command

import aiohttp


class Trust(Command):
    """Trust command."""

    COMMAND = "trust"

    BASE = "https://beam.pro/api/v1/channels/"

    @Command.command(name="list")
    async def list_trusts(self):
        """Get the trused users in a channel."""

        response = await self.api.get_trusts()
        data = await response.json()

        if data["data"] == []:
            return "No trusted user in this channel!"

        return "Trusted users: {}".format(', '.join(
            user["attributes"]["userName"] for user in data["data"]))

    @Command.command()
    async def add(self, user: r'\w{1,32}'):
        """Add a trusted user."""

        response = await aiohttp.get(self.BASE + user)
        if response.status == 404:
            return "User {} does not exist!".format(user)

        data = await response.json()
        user_id = data["id"]
        response = await self.api.trust_user(user_id, user)

        if response.status in (201, 200):
            return "User {} has been trusted!".format(user)

    @Command.command()
    async def remove(self, user: r'\w{1,32}'):
        """Remove a trusted user."""

        response = await aiohttp.get(self.BASE + user)
        if response.status == 404:
            return "User {} does not exist!".format(user)

        data = await response.json()
        user_id = data["id"]
        response = await self.api.remove_trust(user_id)
        print(await response.json())

        if response.status == 200:
            return "Removed trust for user {}!".format(user)
        else:
            return "{} isn't a trusted user".format(user)

    async def get_user_id(self, username):
        return await aiohttp.get(self.BASE + username)
