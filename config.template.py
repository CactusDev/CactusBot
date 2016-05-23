"""CactusBot configuration."""

from .CactusBot.beam import Beam

USERNAME = "BotUsername"
PASSWORD = "p455w0rd"

CHANNEL = "ChannelName"

SERVICE = Beam(USERNAME, PASSWORD, CHANNEL)
