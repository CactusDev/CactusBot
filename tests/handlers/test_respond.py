"""Test the respond handler."""

import pytest

from cactusbot.api import CactusAPI
from cactusbot.handlers import ResponseHandler
from cactusbot.packets import Packet, MessagePacket

response_handler = ResponseHandler()


@pytest.mark.asyncio
async def test_user_update():
    """Test the user update event."""

    assert (await response_handler.on_username_update(Packet(username="TestUser"))
           ) is None

@pytest.mark.asyncio
async def test_on_message():
    """Test the message event."""

    assert (await response_handler.on_message(
        MessagePacket("!testing", user="TestUser")
    )) == StopIteration
