"""CactusBot configuration."""

from CactusBot.services import BeamHandler

USERNAME = "BotUsername"
PASSWORD = "p455w0rd"

CHANNEL = "ChannelName"

SERVICE = BeamHandler(CHANNEL)
