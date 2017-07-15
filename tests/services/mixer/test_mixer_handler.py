import pytest

from cactusbot.handler import Handler, Handlers
from cactusbot.packets import BanPacket, MessagePacket
from cactusbot.services.mixer import MixerHandler


class MixerHandlerWrapper(MixerHandler):

    def __init__(self, handlers):
        self._queue = []
        super().__init__("channel", "token", handlers)

    async def send(self, *args, **kwargs):
        self._queue.append((args, kwargs))

    @property
    def queue(self):
        queue = self._queue
        self._queue = []
        return queue


class PingHandler(Handler):
    async def on_message(self, packet):
        if packet.text == "Ping!":
            return "Pong!"


class SpamHandler(Handler):
    async def on_message(self, packet):
        if "spam" in packet.text:
            return ["No spamming!", BanPacket(packet.user, duration=5)]
        if "SPAM" in packet.text:
            return BanPacket(packet.user)


class FollowHandler(Handler):
    async def on_follow(self, packet):
        return "Thanks for the follow, {}!".format(packet.user)


handlers = Handlers(PingHandler(), SpamHandler(), FollowHandler())
mixer_handler = MixerHandlerWrapper(handlers)


@pytest.mark.asyncio
async def test_handle():

    await mixer_handler.handle("message", "Hello!")
    assert not mixer_handler.queue

    await mixer_handler.handle("message", MessagePacket("Ping!"))
    assert mixer_handler.queue == [(("Pong!",), {})]

    await mixer_handler.handle(
        "message", MessagePacket("spam eggs foo bar", user="Stanley")
    )
    assert mixer_handler.queue == [
        (("No spamming!",), {}),
        (("Stanley", 5), {"method": "timeout"})
    ]


@pytest.mark.asyncio
async def test_handle_chat():

    await mixer_handler.handle_chat({
        'event': 'ChatMessage',
        'data': {
            'id': '688d66e0-352c-11e7-bd11-993537334664',
            'user_level': 111,
            'user_roles': ['Mod', 'Pro', 'User'],
            'message': {
                'message': [{
                    'data': 'Ping!', 'text': 'Ping!', 'type': 'text'
                }],
                'meta': {}
            },
            'channel': 3016,
            'user_id': 2547,
            'user_name': '2Cubed'
        },
        'type': 'event'
    })
    assert mixer_handler.queue == [(("Pong!",), {})]

    await mixer_handler.handle_chat({
        'event': 'ChatMessage',
        'data': {
            'id': '688d66e0-352c-11e7-bd11-993537334664',
            'user_level': 111,
            'user_roles': ['User'],
            'message': {
                'message': [{
                    'data': 'Such spam!', 'text': 'Such spam!', 'type': 'text'
                }],
                'meta': {}
            },
            'channel': 3016,
            'user_id': 2547,
            'user_name': 'Stanley'
        },
        'type': 'event'
    })
    assert mixer_handler.queue == [
        (("No spamming!",), {}),
        (("Stanley", 5), {"method": "timeout"})
    ]


@pytest.mark.asyncio
async def test_handle_constellation():

    await mixer_handler.handle_constellation({
        'event': 'live',
        'data': {
            'payload': {
                'user': {
                    'id': 95845,
                    'avatarUrl': 'https://uploads.beam.pro/avatar/l0icubxz-95845.jpg',
                    'sparks': 2550,
                    'experience': 715,
                    'username': 'Stanley',
                    'verified': True,
                    'deletedAt': None,
                    'channel': {
                        'viewersCurrent': 0,
                        'vodsEnabled': True,
                        'featureLevel': 0,
                        'partnered': False,
                        'interactive': False,
                        'description': None,
                        'name': "Stanley's Channel",
                        'typeId': None,
                        'interactiveGameId': None,
                        'createdAt': '2016-03-05T20:41:21.000Z',
                        'userId': 95845,
                        'bannerUrl': None,
                        'hasTranscodes': True,
                        'hosteeId': None,
                        'suspended': False,
                        'badgeId': None,
                        'numFollowers': 0,
                        'id': 68762,
                        'deletedAt': None,
                        'costreamId': None,
                        'online': False,
                        'languageId': None,
                        'thumbnailId': None,
                        'hasVod': False,
                        'featured': False,
                        'coverId': None,
                        'viewersTotal': 0,
                        'token': 'Stanley',
                        'transcodingProfileId': 1,
                        'updatedAt': '2016-11-13T20:22:01.000Z',
                        'audience': 'teen',
                        'ftl': 0
                    },
                    'createdAt': '2016-03-05T20:41:21.000Z',
                    'bio': None,
                    'updatedAt': '2016-08-20T04:35:25.000Z',
                    'level': 17,
                    'social': {'verified': []},
                    'primaryTeam': None
                },
                'following': True
            },
            'channel': 'channel:3016:followed'
        }, 'type': 'event'})
    assert mixer_handler.queue == [
        (("Thanks for the follow, Stanley!",), {})
    ]
