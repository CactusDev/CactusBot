"""Ban packet."""

from ..packet import Packet


class BanPacket(Packet):

    def __init__(self, *actions, user):
        self.actions = actions
        self.user = user

    def __repr__(self):
        return "<Ban: {}>".format(self.json)

    def __str__(self):
        return "<Ban: {} - {}".format(self.user, self.text)
    
    @property
    def text(self):
        return ''.join(action["action"] for action in self.actions)

    @property
    def json(self):
        return {
            "user": self.user,
            "action": self.actions
        }
