from cactusbot.packets import MessagePacket
from cactusbot.services.mixer.parser import MixerParser


def test_parse_message():

    assert MixerParser.parse_message({
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

    assert MixerParser.parse_message({
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
            'meta': {'me': True}
        },
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

    assert MixerParser.parse_message({
        'channel': 2151,
        'id': '8ef6a160-a9c8-11e6-9c8f-6bd6b629c2eb',
        'message': {
            'message': [{
                'userId': 95845,
                'text': ':Stanleyinaspacesuit',
                'username': 'Stanley',
                'type': 'inaspacesuit'
            }, {
                'text': 'github.com/CactusDev',
                'url': 'http://github.com/CactusDev',
                'type': 'link'
            }, {
                'id': 95845,
                'text': '@Stanley',
                'username': 'Stanley',
                'type': 'tag'
            }],
            'meta': {}
        },
        'user_id': 95845,
        'user_name': 'Stanley',
        'user_roles': ['User']
    }).json == {
        "message": [{
            "type": "emoji",
            "data": "👨‍🚀",
            "text": ":Stanleyinaspacesuit"
        }, {
            "type": "url",
            "data": "http://github.com/CactusDev",
            "text": "github.com/CactusDev"
        }, {
            "type": "tag",
            "data": "Stanley",
            "text": "@Stanley"
        }],
        "user": "Stanley",
        "role": 1,
        "action": False,
        "target": None
    }


def test_parse_follow():

    assert MixerParser.parse_follow({
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

    assert MixerParser.parse_follow({
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

    assert MixerParser.parse_subscribe({
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

    assert MixerParser.parse_resubscribe({
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

    assert MixerParser.parse_host({
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


def test_parse_join():

    assert MixerParser.parse_join({
        'id': 95845,
        'originatingChannel': 2151,
        'username': 'Stanley',
        'roles': ['Mod', 'User']
    }).json == {
        "event": "join",
        "streak": 1,
        "success": True,
        "user": "Stanley"
    }


def test_parse_leave():

    assert MixerParser.parse_leave({
        'id': 95845,
        'originatingChannel': 2151,
        'username': 'Stanley',
        'roles': ['Mod', 'User']
    }).json == {
        "event": "leave",
        "streak": 1,
        "success": True,
        "user": "Stanley"
    }


def test_synthesize():

    assert MixerParser.synthesize(MessagePacket(
        "Hey, ",
        ("tag", "Stanley"),
        "! ",
        ("emoji", "🌵"),
        " Check out ",
        ("url", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
        "!"
    )) == (("Hey, @Stanley! :cactus Check out cactusbot.rtfd.org!",), {})

    assert MixerParser.synthesize(MessagePacket(
        "waves", action=True
    )) == (("/me waves",), {})

    assert MixerParser.synthesize(MessagePacket(
        "Hello!", target="Stanley"
    )) == (("Stanley", "Hello!",), {"method": "whisper"})

    assert MixerParser.synthesize(MessagePacket(
        "Hello! ", ("emoji", "🌵"), "How are you?"
    )) == (("Hello! :cactus How are you?",), {})
