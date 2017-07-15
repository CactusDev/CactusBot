import json

import pytest

from cactusbot.services.mixer import MixerConstellation


class ConstellationWrapper(MixerConstellation):

    def __init__(self, channel, user):
        super().__init__(channel, user)
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

    async def receive(self):
        return {}


constellation = ConstellationWrapper(123, 456)


@pytest.mark.asyncio
async def test_initialize():

    await constellation.initialize("channel:{channel}:update", "user:{user}:followed")
    assert constellation.queue == [{
        "type": "method",
        "method": "livesubscribe",
        "params": {
            "events": ["channel:123:update", "user:456:followed"]
        }
    }]

    await constellation.initialize()
    assert constellation.queue
