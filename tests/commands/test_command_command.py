"""Test the command command."""

import pytest

from tests.api import MockAPI
from cactusbot.commands.magic import Meta
from cactusbot.packets import MessagePacket

command = Meta(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_add():

    packet = MessagePacket(("text", "lol"), ("emoji", "😃"), role=5)
    assert await command("add", "testing", packet, packet=packet) == "Added command !testing."

    packet = MessagePacket("Existing.", role=5)
    assert await command("add", "existing", packet, packet=packet) == "Updated command !existing."


@pytest.mark.asyncio
async def test_remove():

    assert await command("remove", "testing") == "Removed command !testing."

    assert await command("remove", "nonexistent") == "Command !nonexistent does not exist!"


@pytest.mark.asyncio
async def test_list():

    assert await command("list") == "Commands: test, testing"


@pytest.mark.asyncio
async def test_toggle():

    assert await command("enable", "test") == "Command !test has been enabled."
    assert await command("disable", "test") == "Command !test has been disabled."


@pytest.mark.asyncio
async def test_count():

    assert await command("count", "test") == "!test's count is 12."
    assert await command("count", "nonexistent") == "Command !nonexistent does not exist."

    assert await command("count", "test", "50") == "Count updated."
    assert await command("count", "test", "=50") == "Count updated."
    assert await command("count", "test", "+3") == "Count updated."
    assert await command("count", "test", "-1") == "Count updated."
