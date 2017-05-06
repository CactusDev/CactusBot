import pytest

from api import MockAPI
from cactusbot.commands.magic import Alias
from cactusbot.packets import MessagePacket

alias = Alias(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_add():

    assert (await alias("add", "test", "testing", packet=MessagePacket(
        "!alias add test testing", role=5
    ))) == "Alias !test for !testing created."

    assert (await alias("add", "existing", "cmd", packet=MessagePacket(
        "!alias add existing cmd", role=5
    ))) == "Alias !existing for !cmd updated."

    assert (await alias("add", "existing", "cmd", "arg", packet=MessagePacket(
        "!alias add existing cmd arg", role=5
    ))) == "Alias !existing for !cmd updated."

    assert (await alias("add", "thing", "nonexistent", packet=MessagePacket(
        "!alias add thing nonexistent", role=5
    ))) == "Command !nonexistent does not exist."


@pytest.mark.asyncio
async def test_remove():

    assert (await alias("remove", "test", packet=MessagePacket(
        "!alias remove test", role=5
    ))) == "Alias !test removed."

    assert (await alias("remove", "nonexistent", packet=MessagePacket(
        "!alias remove nonexistent", role=5
    ))) == "Alias !nonexistent doesn't exist!"


@pytest.mark.asyncio
async def test_list():

    assert (await alias("list", packet=MessagePacket(
        "!alias list", role=5
    ))) == "Aliases: test (testing)"
