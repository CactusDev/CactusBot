"""Test the multi command."""

import pytest

from cactusbot.api import CactusAPI
from cactusbot.commands.magic import Multi

multi = Multi(CactusAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_multi():
    assert (await multi("b:test", "h:test")).text == (
        "https://multistream.me/b:test/h:test/"
    )

    assert (await multi("fake:test")) == (
        "'fake' is not a valid service."
    )

multi.api.close()
