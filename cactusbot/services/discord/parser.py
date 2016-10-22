import json
from os import path

from ...packets import EditPacket, MessagePacket


class DiscordParser:

    # TODO: roles
    ROLES = {}

    with open(path.join(path.dirname(__file__), "emoji.json")) as file:
        EMOJI = json.load(file)

    @classmethod
    def parse_message(cls, packet):

        message = []
        for component in [packet.content]:
            chunk = {
                "type": "text",
                "data": "",
                "text": component
            }
            message.append(chunk)
            break  # HACK
            # TODO: parsing

        return MessagePacket(
            *message,
            user=packet.author.name,
            role=1,  # TODO
            action=packet.content.startswith(
                '*') and packet.content.endswith('*'),
            target=False  # TODO
        )

    @classmethod
    def parse_edit(cls, old, new):
        return EditPacket(cls.parse_message(old), cls.parse_message(new))

    @classmethod
    def synthesize(cls, packet):
        message = ""
        emoji = dict(zip(cls.EMOJI.values(), cls.EMOJI.keys()))

        for component in packet:
            if component["type"] == "emoji":
                message += emoji.get(component["data"], component["text"])
            elif component["type"] == "link":
                message += component["data"]
            else:
                message += component["text"]

        if packet.action:
            message = '*' + message + '*'

        if packet.target:
            pass  # TODO

        return message
