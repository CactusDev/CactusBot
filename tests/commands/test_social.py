import pytest

from api import MockAPI
from cactusbot.commands.magic import Social

social = Social(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_default():

    assert (await social("a")).text == "A: https://example.com/a"
    assert (await social("a", "b")).text == "A: https://example.com/a, B: https://example.com/b"
    assert await social("invalid") == "'invalid' not found on the streamer's profile!"
    assert await social("valid", "invalid") == "'invalid' not found on the streamer's profile!"

    assert await social(*["test"] * 9) == "Maximum number of requested services (8) exceeded."

    assert (await social()).text == "Test1: https://example.com/test1, Test2: https://example.com/test2"


@pytest.mark.asyncio
async def test_add():

    assert await social("add", "github", "github.com/CactusDev") == "Added social service 'github'."

    assert await social("add", "existing", "example.com") == "Updated social service 'existing'."


@pytest.mark.asyncio
async def test_remove():

    assert await social("remove", "github") == "Removed social service 'github'."

    assert await social("remove", "nonexistent") == "Social service 'nonexistent' doesn't exist!"
