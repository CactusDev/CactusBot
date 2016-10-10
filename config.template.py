"""CactusBot configuration."""

from cactusbot.services.beam.handler import BeamHandler

from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, LoggingHandler,
                                SpamHandler, EventHandler)


USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "TargetName"

# Caches followers to remove chat spam (Default: False)
CACHE_FOLLOWS = False

# How long in minutes before resending message, 0 = never resend
# Only matters if CACHE_FOLLOWS = True (Default: 0)
CACHE_FOLLOWS_TIME = 0


# Don't touch below this line (The code bites)
CACHE_DATA = {
                "CACHE_FOLLOWS":CACHE_FOLLOWS,
                "CACHE_FOLLOWS_TIME":CACHE_FOLLOWS_TIME
                }

handlers = Handlers(LoggingHandler(), EventHandler(CACHE_DATA), 
                    CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)
