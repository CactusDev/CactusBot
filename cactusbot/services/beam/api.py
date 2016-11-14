"""Interact with the Beam API."""

from ..api import API


class BeamAPI(API):
    """Interact with the Beam API."""

    URL = "https://beam.pro/api/v1/"

    async def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        data = {
            "username": username,
            "password": password,
            "code": code
        }
        response = await self.post("/users/login", data=data)
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
