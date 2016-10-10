"""CactusBot configuration."""

from cactusbot.services.beam.handler import BeamHandler

from cactusbot.handler import Handlers
from cactusbot.handlers import CommandHandler, LoggingHandler, SpamHandler, EventHandler


USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "TargetName"

# Caches followers to remove chat spam (Default: False)
CACHE_FOLLOWS = False

handlers = Handlers(LoggingHandler(), EventHandler(), CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)
