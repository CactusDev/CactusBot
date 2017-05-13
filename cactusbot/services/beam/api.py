"""Interact with the Beam API."""

import json

from ..api import API


class BeamAPI(API):
    """Interact with the Beam API."""

    URL = "https://beam.pro/api/v1/"

    headers = {
        "Content-Type": "application/json"
    }

    def __init__(self, channel, token):

        super().__init__()

        self.channel = channel

        self.token = token
        self.headers["Authorization"] = "Bearer {}".format(token)

    async def request(self, method, endpoint, **kwargs):
        """Send HTTP request to an endpoint."""

        if "headers" in kwargs:
            headers = self.headers.copy()
            headers.update(kwargs["headers"])
            kwargs["headers"] = headers
        else:
            kwargs["headers"] = self.headers
        return await super().request(method, endpoint, **kwargs)

    async def get_bot_channel(self, **params):
        """Get the bot's user id."""
        response = await self.get("/users/current", params=params)
        return await response.json()

    async def get_channel(self, channel, **params):
        """Get channel data by username or ID."""
        response = await self.get("/channels/{channel}".format(
            channel=channel), params=params)
        return await response.json()

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        response = await self.get("/chats/{chat}".format(chat=chat))
        return await response.json()

    async def update_roles(self, user, add, remove):
        """Update a user's roles."""

        response = await self.patch("/channels/{channel}/users/{user}".format(
            channel=self.channel, user=user
        ), data=json.dumps({"add": add, "remove": remove}))
        return await response.json()
