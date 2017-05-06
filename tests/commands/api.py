from cactusbot.api import (Alias, CactusAPI, CactusAPIBucket, Command, Repeat,
                           Social)


class MockAPI(CactusAPI):

    def __init__(self, token, password):

        self.token = token
        self.password = password

        self.buckets = {
            "alias": MockAlias(self),
            "command": MockCommand(self),
            "repeat": MockRepeat(self),
            "social": MockSocial(self)
        }


class MockResponse:

    def __init__(self, response, status=200):

        self.response = response
        self.status = status

    async def json(self):
        return self.response


class MockAlias(Alias):

    async def get(self, alias):

        return MockResponse({
            "data": {
                "attributes": {
                    "command": {
                        "count": 1,
                        "enabled": True,
                        "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                        "name": "command_name",
                        "response": {
                            "action": None,
                            "message": [
                                {
                                    "data": "response",
                                    "text": "response",
                                    "type": "text"
                                }
                            ],
                            "role": 1,
                            "target": None,
                            "user": "Stanley"
                        },
                        "token": "cactusdev"
                    },
                    "commandName": "command_name",
                    "name": alias,
                    "token": "cactusdev"
                },
                "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                "type": "alias"
            }
        })

    async def add(self, command, alias, args=None):

        status = 201
        if command == "nonexistent":
            status = 404
        elif alias == "existing":
            status = 200

        return MockResponse({
            "data": {
                "attributes": {
                    "command": {
                        "count": 1,
                        "enabled": True,
                        "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                        "name": command,
                        "response": {
                            "action": False,
                            "message": [
                                {
                                    "data": "response",
                                    "text": "response",
                                    "type": "text"
                                }
                            ],
                            "role": 1,
                            "target": None,
                            "user": "Stanley"
                        },
                        "token": "cactusdev"
                    },
                    "commandName": command,
                    "name": alias,
                    "token": "cactusdev"
                },
                "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                "type": "alias"
            },
            "meta": {
                "edited": True
            }
        }, status=status)

    async def remove(self, alias):

        status = 200
        if alias == "nonexistent":
            status = 404

        return MockResponse({
            "meta": {
                "deleted": [
                    "312ab175-fb52-4a7b-865d-4202176f9234"
                ]
            }
        }, status=status)


class MockCommand(Command):

    async def get(self, name=None):

        if name is not None:
            raise NotImplementedError

        return MockResponse({
            "data": [
                {
                    "attributes": {
                        "count": 2,
                        "enabled": True,
                        "name": "testing",
                        "response": {
                            "action": False,
                            "message": [
                                {
                                    "data": "testing!",
                                    "text": "testing!",
                                    "type": "text"
                                }
                            ],
                            "role": 1,
                            "target": None,
                            "user": "Stanley"
                        },
                        "token": "cactusdev"
                    },
                    "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                    "type": "command"
                },
                {
                    "attributes": {
                        "commandName": "testing",
                        "count": 2,
                        "enabled": True,
                        "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                        "name": "test",
                        "response": {
                            "action": False,
                            "message": [
                                {
                                    "data": "testing!",
                                    "text": "testing!",
                                    "type": "text"
                                }
                            ],
                            "role": 1,
                            "target": None,
                            "user": "Stanley"
                        },
                        "token": "cactusdev"
                    },
                    "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                    "type": "alias"
                }
            ]
        })


class MockRepeat(Repeat):

    async def get(self):

        return MockResponse({
            "data": [
                {
                    "attributes": {
                        "command": "67dd51ee-28e7-4622-9c6a-07ddb0dfc6d8",
                        "commandName": "kittens",
                        "createdAt": "Wed May  3 14:17:49 2017",
                        "period": 600,
                        "repeatName": "kittens",
                        "token": "cactusdev"
                    },
                    "id": "30a57898-bef9-4d4e-a4fc-a276d2f6628c",
                    "type": "repeat"
                }
            ]
        })

    async def add(self, command, period):

        status = 201
        if command == "existing":
            status = 200

        return MockResponse({
            'data': {
                'attributes': {
                    'command': {
                        'count': 6,
                        'enabled': True,
                        'id': '0d1fd105-9574-40fd-be24-2edefd080bf8',
                        'name': command,
                        'response': {
                            'action': False,
                            'message': [{
                                'data': 'response',
                                'text': 'response',
                                'type': 'text'
                            }],
                            'role': 1,
                            'target': None,
                            'user': '2Cubed'
                        },
                        'token': 'cactusdev'
                    },
                    'commandName': command,
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'period': period,
                    'repeatName': command,
                    'token': 'cactusdev'
                },
                'id': 'f45ab1ff-2030-40e7-afda-64591769e74e',
                'type': 'repeat'
            }
        }, status=status)

    async def remove(self, repeat):

        if repeat == "nonexistent":
            return MockResponse(None, status=404)

        return MockResponse({
            'meta': {
                'deleted': ['f45ab1ff-2030-40e7-afda-64591769e74e']
            }
        })


class MockSocial(Social):

    async def get(self, service=None):
        if service is None:
            return MockResponse({
                'data': [{
                    'attributes': {
                        'createdAt': 'Wed May  3 14:17:49 2017',
                        'service': 'test1',
                        'token': 'cactusdev',
                        'url': 'https://example.com/test1'
                    },
                    'id': 'e0522d88-62c7-4c5a-b726-899b2894aaec',
                    'type': 'social'
                }, {
                    'attributes': {
                        'createdAt': 'Wed May  3 14:17:49 2017',
                        'service': 'test2',
                        'token': 'cactusdev',
                        'url': 'https://example.com/test2'
                    },
                    'id': 'e0522d88-62c7-4c5a-b726-899b2894aaed',
                    'type': 'social'
                }]
            })

        if service == "invalid":
            return MockResponse({}, status=404)

        return MockResponse({
            'data': {
                'attributes': {
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'service': service,
                    'token': 'cactusdev',
                    'url': 'https://example.com/' + service
                },
                'id': 'e0522d88-62c7-4c5a-b726-899b2894aaec',
                'type': 'social'
            }
        })

    async def add(self, service, url):

        status = 201
        if service == "existing":
            status = 200

        return MockResponse({
            'data': {
                'attributes': {
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'service': service,
                    'token': 'cactusdev',
                    'url': url
                },
                'id': 'e0522d88-62c7-4c5a-b726-899b2894aaec',
                'type': 'social'
            },
            'meta': {
                'created': True
            }
        }, status=status)

    async def remove(self, service):

        if service == "nonexistent":
            return MockResponse(None, status=404)

        return MockResponse({
            'meta': {
                'deleted': ['e0522d88-62c7-4c5a-b726-899b2894aaec']
            }
        })
