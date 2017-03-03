"""Interact with the Beam API."""

from ..api import API


class BeamAPI(API):
    """Interact with the Beam API."""

    URL = "https://beam.pro/api/v1/"

    headers = {
        "Content-Type": "application/json"
    }

    def authorize(self, token):
        self.token = token

        self.headers["Authorization"] = "Bearer {}".format(token)

    async def get_bot_channel(self, **params):
        """Get the bot's user id."""
        response = await self.get("/users/current", params=params,
                                  headers=self.headers)
        return await response.json()

    async def get_channel(self, channel, **params):
        """Get channel data by username or ID."""
        response = await self.get("/channels/{channel}".format(
            channel=channel), params=params, headers=self.headers)
        return await response.json()

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        response = await self.get("/chats/{chat}".format(chat=chat),
                                  headers=self.headers)
        return await response.json()
