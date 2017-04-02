"""Abstract service class."""

import abc
import logging


class Service(abc.ABC):
    """Abstract service class."""

    def __init__(self, handlers):

        self.logger = logging.getLogger(__name__)

        self.handlers = handlers

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    @abc.abstractmethod
    async def run(self):
        """Run service."""

    async def handle(self, event, packet):
        """Handle incoming events, using :method:`Handlers.handle` ."""

        for response in await self.handlers.handle(event, packet):
            await self.respond(response)

    @abc.abstractmethod
    async def respond(self, response):
        """Respond to a handled packet.

        Parameters
        ----------
        packet : :obj:`Packet`
        """
