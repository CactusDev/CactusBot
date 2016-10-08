"""Action packet."""

from ..packet import Packet

class ActionPacket(Packet):
    
    TYPE = "action"

    def __init__(self, packet_type):
        self.packet_type = packet_type
