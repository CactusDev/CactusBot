"""Ban packet."""

from ..packet import Packet


class BanPacket(Packet):
    """Ban packet."""

    def __init__(self, user, duration=0):
        super().__init__()

        self.user = user
        self.duration = duration

    def __str__(self):
        if self.duration:
            return "<Ban: {}, {} seconds>".format(self.user, self.duration)
        return "<Ban: {}>".format(self.user)

    @property
    def json(self):
        return {
            "user": self.user,
            "duration": self.duration
        }
