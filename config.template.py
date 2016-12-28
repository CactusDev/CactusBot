"""CactusBot configuration."""

from cactusbot.api import CactusAPI
from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, EventHandler, LoggingHandler,
                                SpamHandler)
from cactusbot.services.beam.handler import BeamHandler

USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "ChannelName"

API_TOKEN = "CactusAPI_Token"
api = CactusAPI(API_TOKEN)

# CACHE_FOLLOWS: Cache to remove chat spam (Default: False)
# CACHE_FOLLOWS_TIME: How long in minutes before resending message
#   Leave at 0 for no repeat follow messages
#   Only matters if CACHE_FOLLOWS is enabled (Default: 0)
CACHE_DATA = {
    "CACHE_FOLLOWS": True,
    "CACHE_FOLLOWS_TIME": 0
}


handlers = Handlers(LoggingHandler(), EventHandler(CACHE_DATA, api),
                    SpamHandler(), CommandHandler(CHANNEL, api))

SERVICE = BeamHandler(CHANNEL, handlers)
