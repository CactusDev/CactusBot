from ..packet import Packet

import re


class MessagePacket(Packet):

    TYPE = "message"

    def __init__(self, *message, user="", role=1, action=False):

        message = list(message)
        for index, chunk in enumerate(message):
            if isinstance(chunk, tuple):
                if len(chunk) == 2:
                    chunk = chunk + (chunk[1],)
                message[index] = dict(zip(("type", "data", "text"), chunk))
            elif isinstance(chunk, str):
                message[index] = {"type": "text", "data": chunk, "text": chunk}
        self.message = message

        self.user = user
        self.role = role
        self.action = action

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

    def replace(self, **values):
        for index, chunk in enumerate(self.message):
            if chunk["type"] == "text":
                for old, new in values.items():
                    if new is not None:
                        self.message[index]["text"] = chunk["text"].replace(
                            old, new)
        return self

    def sub(self, pattern, repl):
        for index, chunk in enumerate(self.message):
            if chunk["type"] == "text":
                self.message[index]["text"] = re.sub(
                    pattern, repl, chunk["text"])
        return self
