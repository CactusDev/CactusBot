import json

import pytest

from cactusbot.packets import BanPacket, MessagePacket
from cactusbot.services.mixer import MixerChat


class MixerChatWrapper(MixerChat):

    def __init__(self, channel):
        super().__init__(channel, "endpoint")
        self._queue = []

    async def _send(self, data):
        self._queue.append(json.loads(data))

    @property
    def queue(self):
        queue = self._queue
        self._queue = []
        for item in queue:
            item.pop("id")
        return queue


chat = MixerChatWrapper(238)


async def test_send():

    await chat.send("Hello, world!")
    assert chat.queue == [{
        'arguments': ['Hello, world!'],
        'method': 'msg',
        'type': 'method'
    }]

    await chat.send("This is a reasonably long message.", max_length=10)
    assert chat.queue == [{
        'arguments': ['This is a '], 'method': 'msg', 'type': 'method'
    }, {
        'arguments': ['reasonably'], 'method': 'msg', 'type': 'method'
    }, {
        'arguments': [' long mess'], 'method': 'msg', 'type': 'method'
    }, {
        'arguments': ['age.'], 'method': 'msg', 'type': 'method'
    }]

    await chat.send(238, 123, "authkey", method="auth")
    assert chat.queue == [{
        'arguments': [238, 123, 'authkey'],
        'method': 'auth',
        'type': 'method'
    }]


@pytest.mark.asyncio
async def test_initialize():

    async def get_chat():
        return {"authkey": "AUTHK3Y"}

    await chat.initialize(123, get_chat)
    assert chat.queue == [{
        'arguments': [238, 123, 'AUTHK3Y'],
        'method': 'auth',
        'type': 'method'
    }]

    await chat.initialize()
    assert chat.queue == [{
        "arguments": [238],
        "method": "auth",
        "type": "method"
    }]
