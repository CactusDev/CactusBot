"""Handle handlers."""

class Handlers(object):
    """Handlers."""

    def __init__(self, *handlers):
        self.handlers = handlers

    def handle(self, event, packet):
        """Handle incoming data."""

        for handler in self.handlers:
            if hasattr(handler, "on_" + event):
                response = ""
                try:
                    response = getattr(handler, "on_" + event)(packet)
                except Exception as e:
                    print("Uh oh!")
                    print(e)
                else:
                    if response is StopIteration:
                        break
                    yield response

class Handler(object):
    """Handler."""
    
    def __init__(self):
        self.handlers = Handlers()

    def log(self, message):
        self.handlers.handle("log", message)
