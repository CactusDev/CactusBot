import pytest

from cactusbot.handler import Handler, Handlers
from cactusbot.packets import BanPacket, MessagePacket


class SpamHandler(Handler):
    async def on_message(self, packet):
        if "spam" in packet:
            return [
                MessagePacket("No spamming!", target=packet.user),
                BanPacket(packet.user, duration=1),
                StopIteration
            ]


class EchoHandler(Handler):
    async def on_message(self, packet):
        if packet.text == "break":
            return [12, "working"]
        return packet.text


handlers = Handlers(SpamHandler(), EchoHandler())


@pytest.mark.asyncio
async def test_handlers():

    result = await handlers.handle("message", MessagePacket("spam"))
    assert len(result) == 2
    assert isinstance(result[0], MessagePacket)
    assert isinstance(result[1], BanPacket)

    result = await handlers.handle("message", MessagePacket("break"))
    assert len(result) == 1  # due to invalid packet return type, int
