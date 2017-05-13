"""Test the multi command."""

import pytest

from tests.api import MockAPI
from cactusbot.commands.magic import Multi

multi = Multi(MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_multi():
    assert (await multi("b:test", "h:test")).text == (
        "https://multistream.me/b:test/h:test/"
    )

    assert (await multi("fake:test")) == (
        "'fake' is not a valid service."
    )
