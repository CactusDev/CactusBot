"""Interact with the Twitch API."""

from ..api import API


class TwitchAPI(API):
    """Interact with the Twitch API."""

    URL = "https://api.twitch.tv/api"

    async def get_chat(self, chat):
        """Get required data for connecting to a chat server by channel ID."""
        return await self.get(
            "/channels/{chat}/chat_properties".format(chat=chat))["web_socket_servers"]
