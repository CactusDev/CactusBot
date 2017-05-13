import copy
import json

import pytest

from cactusbot.sepal import Sepal
from test_sepal_parsing import CONFIG_PACKET, REPEAT_PACKET

CONFIG_PACKET = copy.deepcopy(CONFIG_PACKET)
REPEAT_PACKET = copy.deepcopy(REPEAT_PACKET)


class SepalWrapper(Sepal):

    def __init__(self, channel, service):
        super().__init__(channel, service, "endpoint")
        self._queue = []

    async def _send(self, data):
        self._queue.append(json.loads(data))

    @property
    def queue(self):
        queue = self._queue
        self._queue = []
        return queue


class FakeService:

    def __init__(self):
        self._queue = []

    async def handle(self, event, packet):
        self._queue.append(packet)

    @property
    def queue(self):
        queue = self._queue
        self._queue = []
        return queue


sepal = SepalWrapper("channel", FakeService())


@pytest.mark.asyncio
async def test_send():

    await sepal.send("packet_type", key="value")
    assert sepal.queue == [{
        "type": "packet_type",
        "data": {
            "channel": "channel"
        },
        "key": "value"
    }]


@pytest.mark.asyncio
async def test_initialize():

    await sepal.initialize()
    assert sepal.queue == [{
        "type": "join",
        "data": {
            "channel": "channel"
        }
    }]


@pytest.mark.asyncio
async def test_parse():

    assert await sepal._success_function("packet") == "packet"

    assert await sepal.parse('{"key": "value"}') == {"key": "value"}
    assert await sepal.parse("invalid json") is None


@pytest.mark.asyncio
async def test_handle():

    await sepal.handle(REPEAT_PACKET)
    assert len(sepal.service.queue) == 1

    await sepal.handle(CONFIG_PACKET)
    assert len(sepal.service.queue) == 3

    await sepal.handle({"event": "fake"})
    assert not sepal.service.queue

    await sepal.handle({"event": "repeat", "data": {}})
    assert not sepal.service.queue
