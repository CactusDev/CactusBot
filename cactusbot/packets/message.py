"""Message packet."""

import re

from ..packet import Packet


class MessagePacket(Packet):
    """Message packet."""

    def __init__(self, *message, user="", role=1, action=False, target=""):

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
        self.target = target

    def __str__(self):
        return "<Message: {} - \"{}\">".format(self.user, self.text)

    def __len__(self):
        total = 0
        for chunk in self.message:
            total += 1 if chunk["type"] == "emoji" else len(chunk["text"])
        return total

    def __getitem__(self, key):
        return self.text[key]

    def __iter__(self):
        return self.message.__iter__()

    @property
    def text(self):
        """Pure text representation of the packet."""
        return ''.join(chunk["text"] for chunk in self.message)

    @property
    def json(self):
        """JSON representation of the packet."""
        return {
            "message": self.message,
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }

    def replace(self, **values):
        """Replace text in packet."""
        for index, chunk in enumerate(self.message):
            if chunk["type"] == "text":
                for old, new in values.items():
                    if new is not None:
                        self.message[index]["text"] = chunk["text"].replace(
                            old, new)
        return self

    def sub(self, pattern, repl):
        """Perform regex substitution on packet."""
        for index, chunk in enumerate(self.message):
            if chunk["type"] == "text":
                self.message[index]["text"] = re.sub(
                    pattern, repl, chunk["text"])
        return self
