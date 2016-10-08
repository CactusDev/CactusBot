"""Clear packet."""

from ..packet import Packet


class ClearPacket(Packet):

    TYPE = "clear"

    def __init__(self, message=None):
        self.message = message
