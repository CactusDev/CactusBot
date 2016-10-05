"""Handle handlers."""

import logging


class Handlers(object):
    """Handlers."""

    def __init__(self, *handlers):

        self.logger = logging.getLogger(__name__)

        self.handlers = handlers

    def handle(self, event, packet):
        """Handle incoming data."""

        for handler in self.handlers:
            if hasattr(handler, "on_" + event):
                response = ""
                try:
                    response = getattr(handler, "on_" + event)(packet)
                except Exception as e:
                    self.logger.warning(e)
                else:
                    if response is StopIteration:
                        break
                    yield response

class Handler(object):
    """Handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
