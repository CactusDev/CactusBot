"""Handle handlers."""

import logging

from .packet import Packet


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
                    if isinstance(response, Packet):
                        yield response
                    elif isinstance(response, (tuple, list)):
                        yield from response
                    elif response is StopIteration:
                        return


class Handler(object):
    """Handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
