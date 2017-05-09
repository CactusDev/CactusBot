import pytest

from api import MockAPI
from cactusbot.commands.magic import Repeat

repeat = Repeat(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_add():

    assert await repeat("add", "600", "kittens") == "Repeat !kittens added on interval 600."
    assert await repeat("add", "600", "existing") == "Repeat !existing updated with interval 600."

    assert await repeat("add", "twelve", "kittens") == "Invalid 'period': 'twelve'."


@pytest.mark.asyncio
async def test_remove():

    assert await repeat("remove", "kittens") == "Repeat for !kittens removed."
    assert await repeat("remove", "nonexistent") == "Repeat for !nonexistent doesn't exist."


@pytest.mark.asyncio
async def test_list():

    assert await repeat("list") == "Active repeats: kittens 600."
