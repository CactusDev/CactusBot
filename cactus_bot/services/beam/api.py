"""Interacts with the Beam API."""

from logging import getLogger

from urllib.parse import urljoin
from aiohttp import ClientSession, ClientHttpProcessingError


class BeamAPI(ClientSession):
    """Interact with the Beam API."""

    PATH = "https://beam.pro/api/v1/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = getLogger(__name__)

    def _build(self, endpoint):
        return urljoin(self.PATH, endpoint.lstrip('/'))

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to Beam."""

        url = self._build(endpoint)

        async with super().request(method, url, **kwargs) as response:
            if not response.status == 200:
                error = "{resp.status} {resp.reason}".format(resp=response)
                self.logger.error(error)
                raise ClientHttpProcessingError(error)
            try:
                return await response.json()
            except ValueError:
                self.logger.warning("Response was not JSON!")
                raise ClientHttpProcessingError("Response was not JSON!")

    async def get(self, endpoint, **kwargs):
        return await self.request("GET", endpoint, **kwargs)

    async def options(self, endpoint, **kwargs):
        return await self.request("OPTIONS", endpoint, **kwargs)

    async def head(self, endpoint, **kwargs):
        return await self.request("HEAD", endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        return await self.request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request("DELETE", endpoint, **kwargs)

    async def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        data = {
            "username": username,
            "password": password,
            "code": code
        }
        return await self.post("/users/login", data=data)

    async def get_channel(self, channel, **params):
        """Get channel data by username or ID."""
        return await self.get(
            "/channels/{channel}".format(channel=channel), params=params)

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        return await self.get("/chats/{chat}".format(chat=chat))

    async def remove_message(self, chat, message):
        """Remove a message from chat by ID."""
        return await self.delete("/chats/{chat}/message/{message}".format(
            chat=chat, message=message))
