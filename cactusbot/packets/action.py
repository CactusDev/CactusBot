"""Action packet."""

from ..packet import Packet

class EventPacket(Packet):
    
    TYPE = "event"

    def __init__(self, event_type, user):
        self.event_type = event_type
        self.user = user

    def __repr__(self):
        return "<Event: {}>".format(self.json)

    def __str__(self):
        return "<Event: {} - {}".format(self.user, self.event_type)

    @property
    def json(self):
        return {
            "user": self.user,
            "event": self.event_type
        }
