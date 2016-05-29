from logging import getLogger

from aiohttp import ClientSession, ClientHttpProcessingError
from urllib.parse import urljoin


class BeamAPI(ClientSession):
    path = "https://beam.pro/api/v1/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = getLogger(__name__)

    def _build(self, endpoint):
        return urljoin(self.path, endpoint.lstrip('/'))

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

    async def get_channel(self, id, **params):
        """Get channel data by username."""
        return await self.get("/channels/{id}".format(id=id), params=params)

    async def get_chat(self, id):
        """Get chat server data."""
        return await self.get("/chats/{id}".format(id=id))

    async def remove_message(self, id, message):
        """Remove a message from chat."""
        return await self.delete("/chats/{id}/message/{message}".format(
            id=id, message=message), method="DELETE")
