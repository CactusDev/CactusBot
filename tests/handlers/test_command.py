import pytest

from cactusbot.handlers import CommandHandler
from cactusbot.packets import MessagePacket


class TestCommandHandler:

    command_handler = CommandHandler("TestChannel")

    def verify(self, message, expected, *args, **kwargs):
        """Verify target substitutions."""
        actual = self.command_handler._inject(
            MessagePacket(message),
            *args, **kwargs
        ).text
        assert actual == expected

    @pytest.mark.asyncio
    async def test_on_message(self):
        assert (await self.command_handler.on_message(
            MessagePacket("!cactus")
        )).text == "Ohai! I'm CactusBot! :cactus:"

    def test_inject_argn(self):

        self.verify(
            "Let's raid %ARG1%!",
            "Let's raid GreatStreamer!",
            "raid", "GreatStreamer"
        )

        self.verify(
            "Let's raid %ARG1%! #%ARG2%",
            "Let's raid GreatStreamer! #ChannelRaid",
            "raid", "GreatStreamer", "ChannelRaid"
        )

        self.verify(
            "Let's raid %ARG1%!",
            "Not enough arguments!",
            "raid"
        )

        self.verify(
            "This is the !%ARG0% command.",
            "This is the !test command.",
            "test", "arg1", "arg2"
        )

    def test_inject_args(self):

        self.verify(
            "Have some %ARGS%!",
            "Have some hamster-powered floofle waffles!",
            "gift", *"hamster-powered floofle waffles".split()
        )

        self.verify(
            "Have some %ARGS%.",
            "Not enough arguments!",
            "give"
        )

    def test_inject_user(self):

        self.verify(
            "Ohai, %USER%!",
            "Ohai, SomeUser!",
            "ohai", username="SomeUser"
        )

        self.verify(
            "Ohai, %USER%!",
            "Ohai, %USER%!",
            "ohai"
        )

    def test_inject_count(self):
        pass

    def test_inject_channel(self):

        self.verify(
            "Welcome to %CHANNEL%'s stream!",
            "Welcome to GreatStreamer's stream!",
            "welcome", channel="GreatStreamer"
        )

        self.verify(
            "Welcome to %CHANNEL%'s stream!",
            "Welcome to %CHANNEL%'s stream!",
            "welcome"
        )
