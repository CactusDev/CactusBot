import pytest

from cactusbot.handlers import SpamHandler
from cactusbot.packets import MessagePacket

async def get_user_id(_):
    return 0


class MockAPI:

    async def get_trust(self, _):

        class Response:
            status = 404

        return Response()

spam_handler = SpamHandler(MockAPI())


@pytest.mark.asyncio
async def test_on_message():

    assert (await spam_handler.on_message(
        MessagePacket("THIS CONTAINS EXCESSIVE CAPITAL LETTERS.")
    ))[0].text == "Please do not spam capital letters."

    assert (await spam_handler.on_message(MessagePacket(
        "This is what one hundred emoji looks like!",
        *(("emoji", "😮"),) * 100
    )))[0].text == "Please do not spam emoji."

    assert (await spam_handler.on_message(MessagePacket(
        "Check out my amazing Twitter!",
        ("link", "twitter.com/CactusDevTeam",
         "https://twitter.com/CactusDevTeam")
    )))[0].text == "Please do not post URLs."

    assert await spam_handler.on_message(
        MessagePacket("PLEASE STOP SPAMMING CAPITAL LETTERS.", role=50)
    ) is None


def test_check_caps():

    assert not spam_handler.check_caps("")
    assert not spam_handler.check_caps("X")
    assert not spam_handler.check_caps("3.14159265358979")

    assert not spam_handler.check_caps(
        "This is a reasonable message!")
    assert not spam_handler.check_caps("WOW, that was incredible!")

    assert spam_handler.check_caps(
        "THIS IS DEFINITELY CAPITALIZED SPAM.")
    assert spam_handler.check_caps(
        "THAT was SO COOL! OMG WOW FANTASTIC!")


def test_check_emoji():

    assert not spam_handler.check_emoji(MessagePacket(
        "This message contains no emoji."
    ))

    assert not spam_handler.check_emoji(MessagePacket(
        "Wow, that was great!", ("emoji", "😄")))

    assert not spam_handler.check_emoji(MessagePacket(
        *(("emoji", "🌵"),) * 6
    ))

    assert not spam_handler.check_emoji(MessagePacket(
        ("emoji", "😃"),
        ("emoji", "😛"),
        ("emoji", "🌵"),
        ("emoji", "🐹"),
        ("emoji", "🥔"),
        ("emoji", "💚")
    ))

    assert spam_handler.check_emoji(MessagePacket(
        *(("emoji", "🌵"),) * 7
    ))

    assert spam_handler.check_emoji(MessagePacket(
        ("emoji", "😃"),
        ("emoji", "😛"),
        ("emoji", "🌵"),
        ("emoji", "🐹"),
        ("emoji", "🥔"),
        ("emoji", "💚"),
        ("emoji", "😎")
    ))

    assert spam_handler.check_emoji(MessagePacket(
        *(("emoji", "😄"),) * 100
    ))


def test_check_urls():

    assert not spam_handler.contains_urls(MessagePacket(
        "This message contains no links."
    ))

    assert not spam_handler.contains_urls(MessagePacket(
        "google.com was not parsed as a link, and is therefore 'fine'."
    ))

    assert spam_handler.contains_urls(MessagePacket(
        "You should go check out ",
        ("link", "cactusbot.rtfd.org", "https://cactusbot.rtfd.org")
    ))
