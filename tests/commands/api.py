from cactusbot.api import CactusAPI, CactusAPIBucket, Social


class MockAPI(CactusAPI):

    def __init__(self, token, password):

        self.token = token
        self.password = password

        self.buckets = {
            "social": MockSocial(self)
        }


class MockResponse:

    def __init__(self, response, status=200):

        self.response = response
        self.status = status

    async def json(self):
        return self.response


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
