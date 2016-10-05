import json


class Packet:
    def __init__(self, packet_type, **kwargs):
        self.TYPE = packet_type
        self.kwargs = kwargs

    def __repr__(self):
        return '<{}: {}>'.format(self.TYPE, json.dumps(self.json))

    @property
    def json(self):
        return self.kwargs
