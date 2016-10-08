"""Ban packet."""

from ..packet import Packet


class BanPacket(Packet):

    def __init__(self, time=0):
        self.time = time
