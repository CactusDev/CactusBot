import pytest
from cactusbot.api import CactusAPI
from cactusbot.commands.command import Command
from cactusbot.handlers import CommandHandler
from cactusbot.packets import MessagePacket

command_handler = CommandHandler(
    "TestChannel", CactusAPI("test_token", "test_password"))


def verify(message, expected, *args, **kwargs):
    """Verify target substitutions."""
    actual = command_handler._inject(
        MessagePacket(
            *message if isinstance(message, list) else (message,)),
        *args, **kwargs
    ).text
    assert actual == expected


@pytest.mark.asyncio
async def test_on_message():
    assert (await command_handler.on_message(
        MessagePacket("!cactus")
    )).text == "Ohai! I'm CactusBot! 🌵"


def test_inject_argn():

    verify(
        "Let's raid %ARG1%!",
        "Let's raid GreatStreamer!",
        "raid", "GreatStreamer"
    )

    verify(
        "Let's raid %ARG1%! #%ARG2%",
        "Let's raid GreatStreamer! #ChannelRaid",
        "raid", "GreatStreamer", "ChannelRaid"
    )

    verify(
        "Let's raid %ARG1%!",
        "Not enough arguments!",
        "raid"
    )

    verify(
        "This is the !%ARG0% command.",
        "This is the !test command.",
        "test", "arg1", "arg2"
    )

    verify(
        "%ARG1|upper% IS AMAZING!",
        "SALAD IS AMAZING!",
        "amazing", "salad", "taco"
    )

    verify(
        "If you reverse %ARG1%, you get %ARG1|reverse%!",
        "If you reverse potato, you get otatop!",
        "reverse", "potato"
    )

    verify(
        ["Let's raid %ARG1%! ", ("url", "beam.pro/%ARG1|tag%")],
        "Let's raid @Streamer! beam.pro/Streamer",
        "raid", "@Streamer"
    )


def test_inject_args():

    verify(
        "Have some %ARGS%!",
        "Have some hamster-powered floofle waffles!",
        "gift", *"hamster-powered floofle waffles".split()
    )

    verify(
        "Have some %ARGS%.",
        "Not enough arguments!",
        "give"
    )

    verify(
        "Here, have some %ARGS=taco salad%!",
        "Here, have some taco salad!",
        "give"
    )

    verify(
        "Here, have some %ARGS=taco salad%!",
        "Here, have some potato salad!",
        "give", "potato", "salad"
    )


def test_inject_user():

    verify(
        "Ohai, %USER%!",
        "Ohai, SomeUser!",
        "ohai", username="SomeUser"
    )

    verify(
        "Ohai, %USER%!",
        "Ohai, %USER%!",
        "ohai"
    )


def test_inject_count():
    pass


def test_inject_channel():

    verify(
        "Welcome to %CHANNEL%'s stream!",
        "Welcome to GreatStreamer's stream!",
        "welcome", channel="GreatStreamer"
    )

    verify(
        "Welcome to %CHANNEL%'s stream!",
        "Welcome to %CHANNEL%'s stream!",
        "welcome"
    )


def test_modify():

    assert command_handler.modify("Para", "upper") == "PARA"
    assert command_handler.modify("hOI", "lower") == "hoi"
    assert command_handler.modify("taco salad", "title") == "Taco Salad"

    assert command_handler.modify("taco", "reverse") == "ocat"

    assert command_handler.modify("@Innectic", "tag") == "Innectic"
    assert command_handler.modify("Innectic", "tag") == "Innectic"
    assert command_handler.modify("", "tag") == ""

    import random
    random.seed(8)

    assert command_handler.modify("potato", "shuffle") == "otapto"
    assert command_handler.modify("", "shuffle") == ""

    assert command_handler.modify("Jello", "reverse", "title") == "Ollej"


###

async def add_title(name):
    """Add 'Potato Master' title to a name."""
    return "Potato Master " + name.title()


class Potato(Command):

    COMMAND = "potato"

    def __init__(self, api, count=0):

        super().__init__(api)

        self.count = count

    @Command.command(name="count")
    async def default(self):
        """The number of potatoes."""
        return "You have {number} potatoes.".format(number=self.count)

    @Command.command()
    async def add(self, number: r'\d+'):
        """Add potatoes."""

        self.count += int(number)
        return "Added {} potatoes.".format(number)

    @Command.command()
    async def eat(self, number: r'\d+', friend: add_title=None, *,
                  user: "username"):
        """Eat potatoes."""

        number = int(number)

        if friend is None:
            return "{user} ate {number} potatoes!".format(
                user=user, number=number)
        return "{friend} ate {number} potatoes!".format(
            friend=friend, number=number)

    @Command.command(role="subscriber")
    async def check(self, *items: False):
        """Check if items are potatoes."""

        if not items:
            return "You are a potato."

        if len(items) > 3:
            return "Too many things™!"

        result = []
        for item in items:
            if item.lower() == "potato":
                result.append("Yes")
            elif item.lower().lstrip('@') == "innectic":
                result.append("Very")
            else:
                result.append("No")
        return ' '.join(result)

    @Command.command()
    class Battery(Command):
        """Potato battery."""

        @Command.command()
        async def default(self, strength: r'[1-9]\d*'=1):
            """Potato battery."""
            if strength == 1:
                return "Potato power!"
            return "Potato power x {}!".format(strength)

    @Command.command(hidden=True)
    class Wizard(Command):
        """Potato wizard."""

        @Command.command()
        async def default(self, *things):
            """Potato wizard."""
            return MessagePacket(
                "waves wand at {} things...".format(len(things)), action=True
            )

    @Command.command()
    class Salad(Command):
        """Potato salad."""

        @Command.command()
        async def make(self, *ingredients):
            """Make potato salad."""
            return "Making potato salad with {}.".format(
                ', '.join(ingredients))

        @Command.command(hidden=True)
        async def taco(self):
            """Taco salad."""
            return "TACO SALAD!?"

potato = Potato(CactusAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_default():

    assert await potato() == "You have 0 potatoes."
    assert await potato("count") == "You have 0 potatoes."

    assert await potato("battery") == "Potato power!"
    assert await potato("battery", "high") == "Invalid 'strength': 'high'."
    assert await potato("battery", "9001") == "Potato power x 9001!"

    assert await potato("salad") == "Not enough arguments. <make>"


@pytest.mark.asyncio
async def test_args():

    assert await potato("add", "100") == "Added 100 potatoes."

    assert await potato("eat") == "Not enough arguments. <number> [friend]"
    assert await potato("eat", "8", username="2Cubed") == "2Cubed ate 8 potatoes!"
    assert await potato(
        "eat", "2", "innectic", username="2Cubed"
    ) == "Potato Master Innectic ate 2 potatoes!"

    assert await potato("check") == "You are a potato."
    assert await potato(
        "check", packet=MessagePacket(role=4)  # moderator
    ) == "You are a potato."
    assert await potato(
        "check", packet=MessagePacket(role=2)  # subscriber
    ) == "You are a potato."
    assert await potato(
        "check", packet=MessagePacket(role=1)  # user
    ) == "Role level 'Subscriber' or higher required."
    assert await potato(
        "check", "carrot", "potato", "onion"
    ) == "No Yes No"
    assert await potato(
        "check", "Innectic", "@Innectic", "taco"
    ) == "Very Very No"
    assert await potato(
        "check", "way", "too", "many", "things"
    ) == "Too many things™!"

    assert await potato("wizard") == "Not enough arguments. <things...>"
    assert (await potato(
        "wizard", "taco", "salad"
    )).text == "waves wand at 2 things..."

    assert await potato(
        "salad", "make"
    ) == "Not enough arguments. <ingredients...>"
    assert await potato(
        "salad", "make", "carrots", "peppers"
    ) == "Making potato salad with carrots, peppers."

    assert await potato("salad", "taco") == "TACO SALAD!?"
