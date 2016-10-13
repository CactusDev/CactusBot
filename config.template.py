"""CactusBot configuration."""

from cactusbot.services.beam.handler import BeamHandler

from cactusbot.handler import Handlers
from cactusbot.handlers import CommandHandler, LoggingHandler, SpamHandler, EventHandler


USERNAME = "BotUsername"
PASSWORD = "p455w0rd"

CHANNEL = "ChannelName"
handlers = Handlers(LoggingHandler(), EventHandler(),
                    CommandHandler(CHANNEL), SpamHandler())

SERVICE = BeamHandler(CHANNEL, handlers)
