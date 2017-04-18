"""Interact with a REST API."""

import json
import logging
from urllib.parse import urljoin

from aiohttp import ClientHttpProcessingError, ClientSession


class API:
    """Interact with a REST API."""

    URL = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger(__name__)

        self.session = ClientSession()

    def _build(self, endpoint):
        return urljoin(self.URL, endpoint.lstrip('/'))

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to an endpoint."""

        url = self._build(endpoint)

        async with self.session.request(method, url, **kwargs) as response:
            try:
                text = await response.text()
            except json.decoder.JSONDecodeError:
                self.logger.warning("Response was not JSON!")
                self.logger.debug(response.text)
                raise ClientHttpProcessingError("Response was not JSON!")
            else:
                self.logger.debug(
                    "%s %s %s:\n%s %s",
                    method, endpoint, kwargs, response.status, text
                )
                return response

    async def get(self, endpoint, **kwargs):
        """HTTP GET request."""
        return await self.request("GET", endpoint, **kwargs)

    async def options(self, endpoint, **kwargs):
        """HTTP OPTIONS request."""
        return await self.request("OPTIONS", endpoint, **kwargs)

    async def head(self, endpoint, **kwargs):
        """HTTP HEAD request."""
        return await self.request("HEAD", endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        """HTTP POST request."""
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        """HTTP PUT request."""
        return await self.request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        """HTTP PATCH request."""
        return await self.request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        """HTTP DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)
