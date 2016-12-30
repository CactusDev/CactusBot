"""Interact with a REST API."""

import json
import logging
from urllib.parse import urljoin

from aiohttp import ClientHttpProcessingError, ClientSession


class API(ClientSession):
    """Interact with a REST API."""

    URL = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger(__name__)

    def _build(self, endpoint):
        return urljoin(self.URL, endpoint.lstrip('/'))

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to an endpoint."""

        url = self._build(endpoint)

        async with super().request(method, url, **kwargs) as response:
            try:
                text = await response.text()
            except json.decoder.JSONDecodeError:
                self.logger.warning("Response was not JSON!")
                self.logger.debug(response.text)
                raise ClientHttpProcessingError("Response was not JSON!")
            else:
                self.logger.debug(text)
                return response

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
