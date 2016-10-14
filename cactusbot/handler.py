"""Handle handlers."""

import logging

from .packet import Packet
from .packets import MessagePacket


class Handlers(object):
    """Handlers."""

    def __init__(self, *handlers):
        self.logger = logging.getLogger(__name__)

        self.handlers = handlers

    def handle(self, event, packet):
        """Handle incoming data."""

        for handler in self.handlers:
            if hasattr(handler, "on_" + event):
                try:
                    response = getattr(handler, "on_" + event)(packet)
                except Exception:
                    self.logger.warning(
                        "Exception in handler %s:", type(handler).__name__,
                        exc_info=1)
                else:
                    yield from self.translate(response, handler)

    def translate(self, packet, handler):
        """Translate handler responses to Packets."""
        if isinstance(packet, Packet):
            yield packet
        elif isinstance(packet, (tuple, list)):
            for component in packet:
                yield from self.translate(component, handler)
        elif isinstance(packet, str):
            yield MessagePacket(packet)
        elif packet is StopIteration:
            return
        elif packet is None:
            pass
        else:
            self.logger.warning("Invalid return type from %s: %s",
                                type(handler).__name__, type(packet).__name__)


class Handler(object):
    """Handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
