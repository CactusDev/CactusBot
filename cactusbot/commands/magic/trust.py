"""Trust command."""

import aiohttp

from ...packets import MessagePacket
from ..command import Command

BASE_URL = "https://beam.pro/api/v1/channels/{username}"


async def check_user(username):
    if username.startswith('@'):
        username = username[1:]
    async with aiohttp.get(BASE_URL.format(username=username)) as response:
        if response.status == 404:
            raise NameError
        return (username, (await response.json())["id"])


class Trust(Command):
    """Trust command."""

    COMMAND = "trust"

    async def get_user_id(self, username):
        return await aiohttp.get(self.BASE + username)

    @Command.command(hidden=True)
    async def default(self, username: check_user):
        """Toggle a trust."""

        user, user_id = username

        is_trusted = (await self.api.get_trust(user_id)).status == 200

        if is_trusted:
            await self.api.remove_trust(user_id)
        else:
            await self.api.add_trust(user_id, user)

        return MessagePacket(
            ("tag", user), " is {modifier} trusted.".format(
                modifier=("now", "no longer")[is_trusted]))

    @Command.command()
    async def add(self, username: check_user):
        """Add a trusted user."""

        user, user_id = username

        response = await self.api.add_trust(user_id, user)

        if response.status in (201, 200):
            return MessagePacket("User ", ("tag", user), " has been trusted.")

    @Command.command()
    async def remove(self, username: check_user):
        """Remove a trusted user."""

        user, user_id = username

        response = await self.api.remove_trust(user_id)

        if response.status == 200:
            return MessagePacket("Removed trust for user ", ("tag", user), '.')
        else:
            return MessagePacket(("tag", user), " is not a trusted user.")

    @Command.command("list")
    async def list_trusts(self):
        """Get the trused users in a channel."""

        data = await (await self.api.get_trust()).json()

        if not data["data"]:
            return "No trusted users."

        return "Trusted users: {}.".format(', '.join(
            user["attributes"]["userName"] for user in data["data"]))
