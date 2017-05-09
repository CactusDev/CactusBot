"""Test the trust command."""

import pytest

from api import MockAPI
from cactusbot.commands.magic.trust import _trust
from cactusbot.packets import MessagePacket

async def check_user(username):
    if username.startswith('@'):
        username = username[1:]
    if username == "invalid":
        raise NameError
    return (username, username)

trust = _trust(check_user)(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_toggle():

    assert (await trust("Stanley")).text == "Stanley is no longer trusted."
    assert (await trust("untrusted")).text == "untrusted is now trusted."


@pytest.mark.asyncio
async def test_add():

    assert (await trust("add", "Stanley")).text == "User Stanley has been trusted."


@pytest.mark.asyncio
async def test_remove():

    assert (await trust("remove", "Stanley")).text == "Removed trust for user Stanley."
    assert (await trust("remove", "untrusted")).text == "untrusted is not a trusted user."


@pytest.mark.asyncio
async def test_list():

    assert await trust("list") == "Trusted users: Stanley."


@pytest.mark.asyncio
async def test_check():

    assert (await trust("check", "Stanley")).text == "Stanley is trusted."
    assert (await trust("check", "untrusted")).text == "untrusted is not trusted."
