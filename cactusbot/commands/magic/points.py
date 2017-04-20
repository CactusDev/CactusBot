"""Handles the in-bot, channel-specific currency"""

from . import Command
from ...packets import MessagePacket
from .helpers import check_user


class Points(Command):
    """Says stuff and does things"""

    COMMAND = "points"

    @Command.command(hidden=True)
    async def default(self, *, username: "username"):
        """Get the current user's current # of points"""
        response = await self.api.points.get(username)
        if response.status == 404:
            count = 0
        elif response.status == 200:
            data = (await response.json())["data"]
            count = data["attributes"]["count"]
        elif response.status != 200:
            return MessagePacket("An error occured! We're sorry about that :(",
                                 target=username)

        return MessagePacket(
            "You have {val} points!".format(val=count), target=username)

    @Command.command()
    async def give(self, username: check_user, amount, *, sender: "username"):
        """Give another user X amount of points"""
        user, _ = username

        # Verify amount is an integer after 1st char
        if not amount.isdigit():
            return MessagePacket("Amount must be an integer", target=sender)

        response = await self.api.points.transfer(user, sender, amount)
        data = await response.json()
        if response.status in (400, 404, 500):
            print(data)
            # if "errors" in data:
            #     print(data["errors"])
            return MessagePacket("An error occured! We're sorry about that :(",
                                 target=sender)
        else:
            data = data["data"]

        return MessagePacket(
            ("tag", sender), " gave ", ("tag", user), " {val} points!".format(
                val=amount
            ))
