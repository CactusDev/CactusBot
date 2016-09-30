"""Handle handlers."""

class Handlers(object):
    """Handlers."""

    def __init__(self, *handlers):
        self.handlers = handlers

    def handle(self, event, packet):
        """Handle incoming data."""

        for handler in self.handlers:
            if hasattr(handler, "on_" + event):
                try:
                    response = getattr(handler, "on_" + event)(packet)
                except Exception:
                    print("Uh oh!")
                
                if response is StopIteration:
                    break

                yield response

class Handler(object):
    """Handler."""
    pass
