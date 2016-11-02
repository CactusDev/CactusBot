"""CactusBot configuration."""

from cactusbot.services.beam.handler import BeamHandler

from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, LoggingHandler,
                                SpamHandler, EventHandler)


USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "ChannelName"

# CACHE_FOLLOWS: Cache to remove chat spam (Default: False)
# CACHE_FOLLOWS_TIME: How long in minutes before resending message
#   Leave at 0 for no repeat follow messages
#   Only matters if CACHE_FOLLOWS is enabled (Default: 0)
CACHE_DATA = {
    "CACHE_FOLLOWS": True,
    "CACHE_FOLLOWS_TIME": 0
}

handlers = Handlers(LoggingHandler(), EventHandler(CACHE_DATA),
                    CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)
