"""Base packet."""

import json


class Packet:
    """Base packet."""

    def __init__(self, packet_type=None, **kwargs):
        self.type = packet_type or type(self).__name__
        self.kwargs = kwargs

    def __repr__(self):
        return '<{}: {}>'.format(self.type, json.dumps(self.json))

    @property
    def json(self):
        """JSON representation of the packet."""
        return self.kwargs
