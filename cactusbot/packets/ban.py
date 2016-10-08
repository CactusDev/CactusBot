"""Ban packet."""

from ..packet import Packet


class BanPacket(Packet):

    def __init__(self, user, time=0):
        self.user = user
        self.time = time

    def __str__(self):
        if self.time:
            return "<Ban: {}, {} seconds>".format(self.user, self.time)
        return "<Ban: {}>".format(self.user)

    @property
    def json(self):
        return {
            "user": self.user,
            "action": self.actions
        }
