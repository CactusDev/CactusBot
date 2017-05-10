import pytest

from cactusbot.handler import Handler, Handlers
from cactusbot.packets import BanPacket, MessagePacket
from cactusbot.services.beam import BeamHandler
from cactusbot.services.beam.parser import BeamParser


def test_parse_message():

    assert BeamParser.parse_message({
        'channel': 2151,
        'id': '7f43cca0-a9c5-11e6-9c8f-6bd6b629c2eb',
        'message': {
            'message': [
                {'data': 'Hello, world!',
                 'text': 'Hello, world!',
                 'type': 'text'}
            ],
            'meta': {}
        },
        'user_id': 2547,
        'user_name': '2Cubed',
        'user_roles': ['Owner']
    }).json == {
        "message": [{
            "type": "text",
            "data": "Hello, world!",
            "text": "Hello, world!"
        }],
        "user": "2Cubed",
        "role": 5,
        "action": False,
        "target": None
    }

    assert BeamParser.parse_message({
        'channel': 2151,
        'id': '8ef6a160-a9c8-11e6-9c8f-6bd6b629c2eb',
        'message': {
            'message': [
                {'data': 'waves ',
                 'text': 'waves ',
                 'type': 'text'},
                {'coords': {'height': 24, 'width': 24, 'x': 72, 'y': 0},
                 'pack': 'default',
                 'source': 'builtin',
                 'text': ':D',
                 'type': 'emoticon'}],
            'meta': {'me': True}},
        'user_id': 95845,
        'user_name': 'Stanley',
        'user_roles': ['User']
    }).json == {
        "message": [{
            "type": "text",
            "data": "waves ",
            "text": "waves "
        }, {
            "type": "emoji",
            "data": "😃",
            "text": ":D"
        }],
        "user": "Stanley",
        "role": 1,
        "action": True,
        "target": None
    }


def test_parse_follow():

    assert BeamParser.parse_follow({
        'following': True,
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/l0icubxz-95845.jpg',
            'bio': None,
            'channel': {
                'audience': 'teen',
                'badgeId': None,
                'coverId': None,
                'createdAt': '2016-03-05T20:41:21.000Z',
                'deletedAt': None,
                'description': None,
                'featured': False,
                'ftl': 0,
                'hasTranscodes': True,
                'hasVod': False,
                'hosteeId': None,
                'id': 68762,
                'interactive': False,
                'interactiveGameId': None,
                'languageId': None,
                'name': "Stanley's Channel",
                'numFollowers': 0,
                'online': False,
                'partnered': False,
                'suspended': False,
                'thumbnailId': None,
                'token': 'Stanley',
                'transcodingProfileId': None,
                'typeId': None,
                'updatedAt': '2016-08-16T02:53:01.000Z',
                'userId': 95845,
                'viewersCurrent': 0,
                'viewersTotal': 0,
                'vodsEnabled': True
            },
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'experience': 401,
            'frontendVersion': None,
            'id': 95845,
            'level': 13,
            'primaryTeam': None,
            'social': {'verified': []},
            'sparks': 2236,
            'updatedAt': '2016-08-20T04:35:25.000Z',
            'username': 'Stanley',
            'verified': True
        }
    }).json == {
        "user": "Stanley",
        "event": "follow",
        "success": True,
        "streak": 1
    }

    assert BeamParser.parse_follow({
        'following': False,
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/l0icubxz-95845.jpg',
            'bio': None,
            'channel': {'audience': 'teen',
                        'badgeId': None,
                        'coverId': None,
                        'createdAt': '2016-03-05T20:41:21.000Z',
                        'deletedAt': None,
                        'description': None,
                        'featured': False,
                        'ftl': 0,
                        'hasTranscodes': True,
                        'hasVod': False,
                        'hosteeId': None,
                        'id': 68762,
                        'interactive': False,
                        'interactiveGameId': None,
                        'languageId': None,
                        'name': "Stanley's Channel",
                        'numFollowers': 0,
                        'online': False,
                        'partnered': False,
                        'suspended': False,
                        'thumbnailId': None,
                        'token': 'Stanley',
                        'transcodingProfileId': None,
                        'typeId': None,
                        'updatedAt': '2016-08-16T02:53:01.000Z',
                        'userId': 95845,
                        'viewersCurrent': 0,
                        'viewersTotal': 0,
                        'vodsEnabled': True},
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'experience': 401,
            'frontendVersion': None,
            'id': 95845,
            'level': 13,
            'primaryTeam': None,
            'social': {'verified': []},
            'sparks': 2236,
            'updatedAt': '2016-08-20T04:35:25.000Z',
            'username': 'Stanley',
            'verified': True
        }
    }).json == {
        "user": "Stanley",
        "event": "follow",
        "success": False,
        "streak": 1
    }


def test_parse_subscribe():

    assert BeamParser.parse_subscribe({
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/20621.jpg',
            'bio': 'Broadcasting Daily at 10 AM PST. Join in on fun with mostly Minecraft.',
            'createdAt': '2015-05-06T05:13:52.000Z',
            'deletedAt': None,
            'experience': 97980,
            'frontendVersion': None,
            'id': 20621,
            'level': 88,
            'primaryTeam': 89,
            'social': {
                'player': 'https://player.me/innectic',
                'twitter': 'https://twitter.com/Innectic',
                'verified': []
            },
            'sparks': 174519,
            'updatedAt': '2016-08-27T02:11:24.000Z',
            'username': 'Innectic',
            'verified': True
        }
    }).json == {
        "user": "Innectic",
        "event": "subscribe",
        "success": True,
        "streak": 1
    }


def test_parse_resubscribe():

    assert BeamParser.parse_resubscribe({
        "totalMonths": 3,
        "user": {
            "level": 88,
            "social": {
                "player": "https://player.me/innectic",
                "twitter": "https://twitter.com/Innectic",
                "verified": []
            },
            "id": 20621,
            "username": 'Innectic',
            "verified": True,
            "experience": 97980,
            "sparks": 174519,
            "avatarUrl": 'https://uploads.beam.pro/avatar/20621.jpg',
            "bio": 'Broadcasting Daily at 10 AM PST. Join in on fun with mostly Minecraft.',
            "primaryTeam": 89,
            "createdAt": '2016-08-27T02:11:24.000Z',
            'updatedAt': '2016-08-27T02:11:24.000Z',
            "deletedAt": None
        },
        "since": '2016-11-12T20:01:55.000Z',
        "until": '2017-03-13T21:02:25.000Z'
    }).json == {
        "user": "Innectic",
        "event": "subscribe",
        "success": True,
        "streak": 3
    }


def test_parse_host():

    assert BeamParser.parse_host({
        'hoster': {
            'audience': 'teen',
            'badgeId': None,
            'coverId': None,
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'description': None,
            'featured': False,
            'ftl': 0,
            'hasTranscodes': True,
            'hasVod': False,
            'hosteeId': 3016,
            'id': 68762,
            'interactive': False,
            'interactiveGameId': None,
            'languageId': None,
            'name': "Stanley's Channel",
            'numFollowers': 0,
            'online': False,
            'partnered': False,
            'suspended': False,
            'thumbnailId': None,
            'token': 'Stanley',
            'transcodingProfileId': None,
            'typeId': None,
            'updatedAt': '2016-11-13T20:21:59.000Z',
            'userId': 95845,
            'viewersCurrent': 0,
            'viewersTotal': 0,
            'vodsEnabled': True},
        'hosterId': 68762
    }).json == {
        "user": "Stanley",
        "event": "host",
        "success": True,
        "streak": 1
    }


def test_synthesize():

    assert BeamParser.synthesize(MessagePacket(
        "Hey, ",
        ("tag", "Stanley"),
        "! ",
        ("emoji", "🌵"),
        " Check out ",
        ("url", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
        "!"
    )) == (("Hey, @Stanley! :cactus Check out cactusbot.rtfd.org!",), {})

    assert BeamParser.synthesize(MessagePacket(
        "waves", action=True
    )) == (("/me waves",), {})

    assert BeamParser.synthesize(MessagePacket(
        "Hello!", target="Stanley"
    )) == (("Stanley", "Hello!",), {"method": "whisper"})


class BeamHandlerWrapper(BeamHandler):

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
            return ("No spamming!", BanPacket(packet.user, duration=5))
        if "SPAM" in packet.text:
            return BanPacket(packet.user)


class FollowHandler(Handler):
    async def on_follow(self, packet):
        return "Thanks for the follow, {}!".format(packet.user)


handlers = Handlers(PingHandler(), SpamHandler(), FollowHandler())
beam_handler = BeamHandlerWrapper(handlers)


@pytest.mark.asyncio
async def test_handle():

    await beam_handler.handle("message", "Hello!")
    assert not beam_handler.queue

    await beam_handler.handle("message", MessagePacket("Ping!"))
    assert beam_handler.queue == [(("Pong!",), {})]

    await beam_handler.handle(
        "message", MessagePacket("spam eggs foo bar", user="Stanley")
    )
    assert beam_handler.queue == [
        (("No spamming!",), {}),
        (("Stanley", 5), {"method": "timeout"})
    ]


@pytest.mark.asyncio
async def test_handle_chat():

    await beam_handler.handle_chat({
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
    assert beam_handler.queue == [(("Pong!",), {})]

    await beam_handler.handle_chat({
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
    assert beam_handler.queue == [
        (("No spamming!",), {}),
        (("Stanley", 5), {"method": "timeout"})
    ]


@pytest.mark.asyncio
async def test_handle_constellation():

    await beam_handler.handle_constellation({
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
    assert beam_handler.queue == [
        (("Thanks for the follow, Stanley!",), {})
    ]
