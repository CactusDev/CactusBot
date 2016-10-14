"""Base packet."""

import json


class Packet:
    """Base packet."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        return '<{}: {}>'.format(
            type(self).__name__.title(), json.dumps(self.json))

    @property
    def json(self):
        """JSON representation of the packet."""
        return self.kwargs
