"""Cactus command."""


from . import Command
from ...packets import MessagePacket


class Cactus(Command):
    """Ouch! That's pokey!"""

    COMMAND = "cactus"

    @Command.subcommand
    async def cactus(self):
        return MessagePacket("Ohai! I'm CactusBot! ", ("emoji", "🌵"))

    @Command.subcommand
    async def docs(self):
        return MessagePacket(
            "Check out my documentation at ",
            ("url", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
            "."
        )

    @Command.subcommand
    async def twitter(self):
        return MessagePacket(
            ("text", "You can follow the team behind CactusBot at: "),
            ("url", "https://twitter.com/CactusDevTeam",
             "twitter.com/CactusDevTeam")
        )

    @Command.subcommand
    async def help(self):
        return ("Try our docs (!cactus docs). If that doesn't help, tweet at"
                " us (!cactus twitter)!")

    DEFAULT = cactus
