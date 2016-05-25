from logging import getLogger

from aiohttp import ClientSession
from urllib.parse import urljoin


class BeamAPI(object):
    path = "https://beam.pro/api/v1/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = getLogger(__name__)

        self.session = ClientSession()

    async def _request(self, endpoint, method="GET", **kwargs):
        """Send HTTP request to Beam."""
        url = urljoin(self.path, endpoint.lstrip('/'))
        async with self.session.request(method, url, **kwargs) as response:
            try:
                return await response.json()
            except ValueError:
                return await response.text()

    async def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        data = {
            "username": username,
            "password": password,
            "code": code
        }
        return await self._request("/users/login", method="POST", data=data)

    async def get_channel(self, id, **params):  # TODO: add explosions
        """Get channel data by username."""
        return await self._request(
            "/channels/{id}".format(id=id), params=params)

    async def get_chat(self, id):  # TODO: add explosions
        """Get chat server data."""
        return await self._request("/chats/{id}".format(id=id))

    async def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return await self._request("/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id), method="DELETE")
