import pytest

from api import MockAPI
from cactusbot.commands.magic import Quote

quote = Quote(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_get():

    assert await quote() == '"Quote!" -Someone'

    assert await quote("8") == '"Quote!" -Someone'
    assert await quote("123") == "Quote 123 does not exist!"


@pytest.mark.asyncio
async def test_add():
    assert await quote("add", "Hello!") == "Added quote #8."


@pytest.mark.asyncio
async def test_edit():
    assert await quote("edit", "7", "Hi!") == "Edited quote #7."
    assert await quote("edit", "8", "Hi!") == "Added quote #8."


@pytest.mark.asyncio
async def test_remove():
    assert await quote("remove", "7") == "Removed quote #7."
    assert await quote("remove", "8") == "Quote #8 does not exist!"
