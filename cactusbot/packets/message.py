from ..packet import Packet


class MessagePacket(Packet):

    TYPE = "message"

    def __init__(self, *message, user, role=1, **meta):

        message = list(message)
        for index, chunk in enumerate(message):
            if isinstance(chunk, tuple):
                if len(chunk) == 2:
                    chunk = chunk + (chunk[1],)
                message[index] = dict(zip(("type", "data", "text"), chunk))
        self.message = tuple(message)

        self.user = user
        self.role = role
        self.meta = meta

    def __repr__(self):
        return "<Message: {}>".format(self.json)

    def __str__(self):
        return "<Message: {} - \"{}\">".format(self.user, self.text)

    def __len__(self):
        total = 0
        for chunk in self.message:
            total += 1 if chunk["type"] == "emoticon" else len(chunk["text"])
        return total

    def __getitem__(self, key):
        return self.text[key]

    def __iter__(self):
        return self.message.__iter__()

    @property
    def text(self):
        return ''.join(chunk["text"] for chunk in self.message)

    @property
    def json(self):
        return {
            "user": self.user,
            "role": self.role,
            "message": self.message
        }
