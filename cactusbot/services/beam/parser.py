from ...packets import MessagePacket, EventPacket

import json
from os import path


class BeamParser:

    ROLES = {
        "Owner": 100,
        "Founder": 91,
        "Staff": 90,
        "Global Mod": 85,
        "Mod": 50,
        "Subscriber": 20,
        "Pro": 5,
        "User": 1,
        "Muted": 0,
        "Banned": -1
    }

    with open(path.join(path.dirname(__file__), "emoji.json")) as file:
        EMOJI = json.load(file)

    @classmethod
    def parse_message(cls, packet):

        message = []
        for component in packet["message"]["message"]:
            chunk = {
                "type": component["type"],
                "data": "",
                "text": component["text"]
            }
            if component["type"] == "emoticon":
                chunk["type"] = "emoji"
                chunk["data"] = cls.EMOJI.get(component["text"], "")
                message.append(chunk)
            elif component["type"] == "link":
                chunk["data"] = component["url"]
                message.append(chunk)
            elif component["type"] == "tag":
                chunk["data"] = component["username"]
                message.append(chunk)
            elif component["text"]:
                chunk["data"] = component["text"]
                message.append(chunk)

        return MessagePacket(
            *message,
            user=packet["user_name"],
            role=cls.ROLES[packet["user_roles"][0]],
            action=packet["message"]["meta"].get("me", False),
            target=packet["message"]["meta"].get(
                "whisper", "") and packet["target"]
        )

    @classmethod
    def parse_follow(cls, packet):
        return EventPacket(
            "follow",
            packet["user"]["username"],
            packet["following"]
        )

    @classmethod
    def parse_subscribe(cls, packet):
        return EventPacket("subscribe", packet["user"]["username"])

    @classmethod
    def parse_host(cls, packet):
        return EventPacket(
            "host",
            packet["user"]["username"],
            packet["hosting"]
        )

    @classmethod
    def synthesize(cls, packet):
        message = ""
        emoji = dict(zip(cls.EMOJI.values(), cls.EMOJI.keys()))

        if packet.action:
            message = "/me "

        for component in packet:
            if component["type"] == "emoji":
                message += emoji.get(component["data"], component["text"])
            else:
                message += component["text"]

        if packet.target:
            return (packet.target, message), {"method": "whisper"}

        return (message,), {}
