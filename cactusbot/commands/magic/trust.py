"""Trust command."""

import aiohttp

from ...packets import MessagePacket
from ..command import Command

BASE_URL = "https://beam.pro/api/v1/channels/{username}"


async def check_beam_user(username):
    """Check if a Beam username exists."""
    if username.startswith('@'):
        username = username[1:]
    async with aiohttp.get(BASE_URL.format(username=username)) as response:
        if response.status == 404:
            raise NameError
        return (username, (await response.json())["id"])


def _trust(check_user=check_beam_user):

    class Trust(Command):  # pylint: disable=W0621
        """Trust command."""

        COMMAND = "trust"
        ROLE = "moderator"

        @Command.command(hidden=True)
        async def default(self, username: check_user):
            """Toggle a trust."""

            user, user_id = username

            is_trusted = (await self.api.trust.get(user_id)).status == 200

            if is_trusted:
                await self.api.trust.remove(user_id)
            else:
                await self.api.trust.add(user_id, user)

            return MessagePacket(
                ("tag", user), " is {modifier} trusted.".format(
                    modifier=("now", "no longer")[is_trusted]))

        @Command.command()
        async def add(self, username: check_user):
            """Add a trusted user."""

            user, user_id = username

            response = await self.api.trust.add(user_id, user)

            if response.status in (201, 200):
                return MessagePacket(
                    "User ", ("tag", user), " has been trusted.")

        @Command.command()
        async def remove(self, username: check_user):
            """Remove a trusted user."""

            user, user_id = username

            response = await self.api.trust.remove(user_id)

            if response.status == 200:
                return MessagePacket(
                    "Removed trust for user ", ("tag", user), '.')
            return MessagePacket(("tag", user), " is not a trusted user.")

        @Command.command(name="list")
        async def list_trusts(self):
            """Get the trused users in a channel."""

            data = await (await self.api.trust.get()).json()

            if not data["data"]:
                return "No trusted users."

            return "Trusted users: {}.".format(', '.join(
                user["attributes"]["userName"] for user in data["data"]))

        @Command.command()
        async def check(self, username: check_user):
            """Check if a user is currently trusted in the channel."""

            user, user_id = username

            data = await (await self.api.trust.get(user_id)).json()

            return MessagePacket(("tag", user), " is {status}trusted.".format(
                status="" if data["data"] else "not "))

    return Trust


Trust = _trust()
