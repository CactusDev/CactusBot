"""Message packet."""

import re

from ..packet import Packet


class MessagePacket(Packet):
    """Message packet."""

    def __init__(self, *message, user="", role=1, action=False, target=None):
        super().__init__()

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
        return len(''.join(
            chunk["text"] for chunk in self.message
            if chunk["type"] == "text"
        ))

    def __getitem__(self, key):

        if isinstance(key, int):
            return ''.join(
                chunk["text"] for chunk in self.message
                if chunk["type"] == "text"
            )[key]

        elif isinstance(key, slice):

            if key.stop is not None or key.step is not None:
                raise NotImplementedError  # TODO

            count = key.start or 0
            message = self.message.copy()

            for component in message.copy():
                if component["type"] == "text":
                    if len(component["text"]) <= count:
                        count -= len(component["text"])
                        message.pop(0)
                    else:
                        while count > 0:
                            component["text"] = component["text"][1:]
                            component["data"] = component["data"][1:]
                            count -= 1
                else:
                    message.pop(0)
                if count == 0:
                    return self.copy(*message)
            return self.copy(*message)

        raise TypeError

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

    def copy(self, *args, **kwargs):
        """Return a copy."""

        _args = args or self.message

        _kwargs = {
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }
        _kwargs.update(kwargs)

        return MessagePacket(*_args, **_kwargs)

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

    def split(self, seperator=' ', maximum=None):
        """Split into multiple MessagePackets, based on a separator."""

        result = []
        components = []

        if maximum is None:
            maximum = float('inf')

        for component in self:

            if len(result) == maximum:
                components.append(component)
                continue

            is_text = component["type"] == "text"
            if not is_text or seperator not in component["text"]:
                components.append(component)
                continue

            new = {"type": "text", "text": "", "data": ""}

            for index, character in enumerate(component["text"]):
                if len(result) == maximum:
                    new["data"] = new["text"] = \
                        new["text"] + component["text"][index:]
                    break

                if character == seperator:
                    components.append(new.copy())
                    result.append(components.copy())
                    components.clear()
                    new["data"] = new["text"] = ""
                else:
                    new["data"] = new["text"] = new["text"] + character

            components.append(new)

        result.append(components)

        return [self.copy(*message) for message in result]
