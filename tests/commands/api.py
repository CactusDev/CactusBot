from cactusbot.api import (Alias, CactusAPI, Command, Config, Quote, Repeat,
                           Social, Trust)


class MockAPI(CactusAPI):

    def __init__(self, token, password):

        self.token = token
        self.password = password

        self.buckets = {
            "alias": MockAlias(self),
            "command": MockCommand(self),
            "config": MockConfig(self),
            "quote": MockQuote(self),
            "repeat": MockRepeat(self),
            "social": MockSocial(self),
            "trust": MockTrust(self)
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


class MockConfig(Config):

    async def get(self, *keys):

        if keys:
            raise NotImplementedError

        return MockResponse({
            'data': {
                'attributes': {
                    'announce': {
                        'follow': {
                            'announce': True,
                            'message': 'Thanks for the follow, %USER%!'
                        },
                        'host': {
                            'announce': True,
                            'message': 'Thanks for the host, %USER%!'
                        },
                        'join': {
                            'announce': False,
                            'message': 'Welcome, %USER%!'
                        },
                        'leave': {
                            'announce': False,
                            'message': 'Thanks for watching, %USER%!'
                        },
                        'sub': {
                            'announce': True,
                            'message': 'Thanks for the subscription, %USER%!'
                        }
                    },
                    'services': [{
                        'isOAuth': False,
                        'name': 'beam',
                        'permissions': ['chat:connect', 'chat:chat'],
                        'username': 'CactusBot'
                    }],
                    'spam': {
                        'allowUrls': True,
                        'maxCapsScore': 16,
                        'maxEmoji': 6
                    },
                    'token': 'cactusdev',
                    'whitelistedUrls': []
                },
                'id': '2d1976ca-d2fe-4b95-a9fa-e9bac4fe9cfa',
                'type': 'config'
            }
        })

    async def update(self, value):
        return MockResponse(value)


class MockQuote(Quote):

    async def get(self, quote_id=None):

        if quote_id == "123":
            return MockResponse({'data': {}}, status=404)

        response = {
            'data': {
                'attributes': {
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'quote': '"Quote!" -Someone',
                    'quoteId': quote_id if quote_id is not None else 8,
                    'token': 'cactusdev'
                },
                'id': '9f8421c7-8e54-4ca7-9a68-b2cb6e8626e5',
                'type': 'quote'
            }
        }

        if quote_id is None:
            response["data"] = [response["data"]]

        return MockResponse(response)

    async def add(self, quote):
        return MockResponse({
            'data': {
                'attributes': {
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'quote': quote,
                    'quoteId': 8,
                    'token': 'cactusdev'
                },
                'id': '9f8421c7-8e54-4ca7-9a68-b2cb6e8626e5',
                'type': 'quote'
            }
        })

    async def edit(self, quote_id, quote):

        status = 200
        if quote_id == "8":
            status = 201

        return MockResponse({
            'data': {
                'attributes': {
                    'createdAt': 'Wed May  3 14:17:49 2017',
                    'quote': quote,
                    'quoteId': quote_id,
                    'token': 'cactusdev'
                },
                'id': '9f8421c7-8e54-4ca7-9a68-b2cb6e8626e5',
                'type': 'quote'
            }
        }, status=status)

    async def remove(self, quote_id):

        status = 200
        if quote_id == "8":
            status = 404

        return MockResponse({
            'meta': {
                'deleted': ['50983973-cd75-442e-ad71-1a9e194b51c4']
            }
        }, status=status)


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


class MockTrust(Trust):

    async def get(self, user_id=None):

        if user_id is not None:

            if user_id == "untrusted":
                return MockResponse({"data": {}}, status=404)

            return MockResponse({
                "data": {
                    "attributes": {
                        "token": "cactusdev",
                        "userId": user_id,
                        "userName": "Stanley"
                    }
                }
            })

        return MockResponse({
            "data": [{
                "attributes": {
                    "token": "cactusdev",
                    "userId": "95845",
                    "userName": "Stanley"
                }
            }]
        })

    async def add(self, user_id, username):

        return MockResponse({
            "attributes": {
                "attributes": {
                    "token": "cactusdev",
                    "userId": user_id,
                    "userName": username
                },
                "id": "7875b898-fbb3-426f-aca3-7375d97326b0",
                "type": "trust"
            },
            "meta": {
                "created": True
            }
        })

    async def remove(self, user_id):

        status = 200
        if user_id == "untrusted":
            status = 404

        return MockResponse({
            "meta": {
                "deleted": [
                    "7875b898-fbb3-426f-aca3-7375d97326b0"
                ]
            }
        }, status=status)
