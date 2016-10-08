"""Action packet."""

from ..packet import Packet

class ActionPacket(Packet):
    
    TYPE = "action"

    def __init__(self, packet_type, user):
        self.packet_type = packet_type
        self.user = user

    def __repr__(self):
        return "<Action: {}>".format(self.json)

    def __str__(self):
        return "<Action: {} - {}".format(self.user, self.packet_type)

    @property
    def json(self):
        return {
            "user": self.user,
            "action": self.packet_type
        }
