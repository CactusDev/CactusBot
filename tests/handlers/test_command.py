import pytest

from cactusbot.handlers import CommandHandler
from cactusbot.packets import MessagePacket


class TestCommandHandler:

    command_handler = CommandHandler("TestChannel")

    @pytest.mark.asyncio
    async def test_on_message(self):
        assert (await self.command_handler.on_message(
            MessagePacket("!cactus")
        )).text == "Ohai! I'm CactusBot! :cactus:"

    def test_inject_argn(self):
        assert self.command_handler.inject(
            MessagePacket("Let's raid %ARG1%!"),
            "raid", "GreatStreamer"
        ).text == "Let's raid GreatStreamer!"

        assert self.command_handler.inject(
            MessagePacket("Let's raid %ARG1%! #%ARG2%"),
            "raid", "GreatStreamer", "ChannelRaid"
        ).text == "Let's raid GreatStreamer! #ChannelRaid"

        assert self.command_handler.inject(
            MessagePacket("Let's raid %ARG1%!"),
            "raid"
        ).text == "Not enough arguments!"

        assert self.command_handler.inject(
            MessagePacket("This is the !%ARG0% command."),
            "test", "arg1", "arg2"
        ).text == "This is the !test command."

    def test_inject_args(self):
        assert self.command_handler.inject(
            MessagePacket("Have some %ARGS%!"),
            "gift", *"hamster-powered floofle waffles".split()
        ).text == "Have some hamster-powered floofle waffles!"

        assert self.command_handler.inject(
            MessagePacket("Have some %ARGS%."),
            "give"
        ).text == "Not enough arguments!"

    def test_inject_user(self):
        assert self.command_handler.inject(
            MessagePacket("Ohai, %USER%!"),
            "ohai", username="SomeUser"
        ).text == "Ohai, SomeUser!"

        assert self.command_handler.inject(
            MessagePacket("Ohai, %USER%!"),
            "ohai"
        ).text == "Ohai, %USER%!"

    def test_inject_count(self):
        pass

    def test_inject_channel(self):
        assert self.command_handler.inject(
            MessagePacket("Welcome to %CHANNEL%'s stream'!"),
            "welcome", channel="GreatStreamer"
        ).text == "Welcome to GreatStreamer's stream'!"

        assert self.command_handler.inject(
            MessagePacket("Welcome to %CHANNEL%'s stream'!"),
            "welcome",
        ).text == "Welcome to %CHANNEL%'s stream'!"
