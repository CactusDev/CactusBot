"""CactusBot configuration."""

from cactusbot.api import CactusAPI
from cactusbot.handler import Handlers
from cactusbot.handlers import (CommandHandler, EventHandler, LoggingHandler,
                                ResponseHandler, SpamHandler)
from cactusbot.services.beam.handler import BeamHandler

TOKEN = "OAuth_Token"
CHANNEL = "ChannelName"

API_TOKEN = "CactusAPI_Token"
API_PASSWORD = "CactusAPI_Password"

API_URL = "https://cactus.exoz.one/api/v1/"
SEPAL_URL = "wss://cactus.exoz.one/sepal"

api = CactusAPI(API_TOKEN, API_PASSWORD, url=API_URL)


CACHE_DATA = {
    "cache_follow": True,
    "cache_host": True,
    "cache_join": True,
    "cache_leave": True,
    "cache_time": 1200
}


handlers = Handlers(
    LoggingHandler(),
    ResponseHandler(),
    EventHandler(CACHE_DATA, api),
    SpamHandler(api),
    CommandHandler(CHANNEL, api)
)

SERVICE = BeamHandler(CHANNEL, TOKEN, handlers)
