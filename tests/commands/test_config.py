import pytest

from api import MockAPI
from cactusbot.commands.magic import Config

config = Config(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_announce_default():

    assert await config("follow") == "Enabled, message: 'Thanks for the follow, %USER%!'"
    assert await config("follow", "enable") == "Follow announcements are now enabled."
    assert await config("follow", "disable") == "Follow announcements are now disabled."
    assert await config("follow", "potato") == "Invalid boolean value: 'potato'."

    assert await config("subscribe") == "Enabled, message: 'Thanks for the subscription, %USER%!'"
    assert await config("subscribe", "enable") == "Subscribe announcements are now enabled."
    assert await config("subscribe", "disable") == "Subscribe announcements are now disabled."
    assert await config("subscribe", "potato") == "Invalid boolean value: 'potato'."

    assert await config("host") == "Enabled, message: 'Thanks for the host, %USER%!'"
    assert await config("host", "enable") == "Host announcements are now enabled."
    assert await config("host", "disable") == "Host announcements are now disabled."
    assert await config("host", "potato") == "Invalid boolean value: 'potato'."

    assert await config("leave") == "Disabled, message: 'Thanks for watching, %USER%!'"
    assert await config("leave", "enable") == "Leave announcements are now enabled."
    assert await config("leave", "disable") == "Leave announcements are now disabled."
    assert await config("leave", "potato") == "Invalid boolean value: 'potato'."

    assert await config("join") == "Disabled, message: 'Welcome, %USER%!'"
    assert await config("join", "enable") == "Join announcements are now enabled."
    assert await config("join", "disable") == "Join announcements are now disabled."
    assert await config("join", "potato") == "Invalid boolean value: 'potato'."


@pytest.mark.asyncio
async def test_announce_message():

    assert await config("follow", "message") == "Current response: 'Thanks for the follow, %USER%!'"
    assert await config("follow", "message", "Thanks!") == "Set new follow message response."

    assert await config("subscribe", "message") == "Current response: 'Thanks for the subscription, %USER%!'"
    assert await config("subscribe", "message", "Thanks!") == "Set new subscribe message response."

    assert await config("host", "message") == "Current response: 'Thanks for the host, %USER%!'"
    assert await config("host", "message", "Thanks!") == "Set new host message response."

    assert await config("leave", "message") == "Current response: 'Thanks for watching, %USER%!'"
    assert await config("leave", "message", "Thanks!") == "Set new leave message response."

    assert await config("join", "message") == "Current response: 'Welcome, %USER%!'"
    assert await config("join", "message", "Thanks!") == "Set new join message response."


@pytest.mark.asyncio
async def test_spam_default():

    assert await config("spam", "urls") == "URLs are allowed."
    assert await config("spam", "urls", "enable") == "URLs are now allowed."
    assert await config("spam", "urls", "disable") == "URLs are now disallowed."
    assert await config("spam", "urls", "potato") == "Invalid boolean value: 'potato'."

    assert await config("spam", "emoji") == "Maximum amount of emoji allowed is 6."
    assert await config("spam", "emoji", "8") == "Maximum amount of emoji updated to 8."

    assert await config("spam", "caps") == "Maximum capitals score is 16."
    assert await config("spam", "caps", "17") == "Maximum capitals score is now 17."
