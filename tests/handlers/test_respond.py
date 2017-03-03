"""Test the respond handler."""

import pytest

from cactusbot.api import CactusAPI
from cactusbot.handlers import ResponseHandler
from cactusbot.packets import MessagePacket

response_handler = ResponseHandler("TestUser")


@pytest.mark.asyncio
async def test_on_message():
    """Test the message event."""

    assert (await response_handler.on_message(
        MessagePacket("!testing", user="TestUser")
    )) == StopIteration
