from ..packet import Packet


class MessagePacket(Packet):

    TYPE = "message"

    def __init__(self, *message, user, role=1, **meta):
        self.message = message
        self.user = user
        self.role = role
        self.meta = meta

    def __len__(self):
        total = 0
        for chunk in self.message:
            if chunk["type"] == "emoticon":
                total += 1
            else:
                total += len(chunk["text"])
        return total

    def __getitem__(self, key):
        return self._str[key]

    @property
    def _str(self):
        return ''.join(chunk["text"] for chunk in self.message)

    @property
    def json(self):
        return {
            "user": self.user,
            "role": self.role,
            "message": self.message
        }
