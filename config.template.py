"""CactusBot configuration."""

from CactusBot.services import Beam

USERNAME = "BotUsername"
PASSWORD = "p455w0rd"

CHANNEL = "ChannelName"

SERVICE = Beam(USERNAME, PASSWORD, CHANNEL)
