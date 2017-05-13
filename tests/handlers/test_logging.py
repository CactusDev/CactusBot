import pytest

from cactusbot.handlers import LoggingHandler
from cactusbot.packets import EventPacket, MessagePacket

logging_handler = LoggingHandler()


@pytest.mark.asyncio
async def test_logging():

    await logging_handler.on_message(MessagePacket("Hello!", user="Stanley"))
    await logging_handler.on_join(EventPacket("join", "Stanley"))
    await logging_handler.on_leave(EventPacket("leave", "Stanley"))
    await logging_handler.on_follow(EventPacket("follow", "Stanley"))
    await logging_handler.on_subscribe(EventPacket("subscribe", "Stanley"))
    await logging_handler.on_resubscribe(EventPacket("subscribe", "Stanley"))
    await logging_handler.on_host(EventPacket("subscribe", "Stanley"))
