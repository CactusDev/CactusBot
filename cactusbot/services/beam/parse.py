"""Parse Beam packets."""

import json
from os import path

from ...packets import EventPacket, MessagePacket

ROLES = {
    "Owner": 5,
    "Staff": 4,  # Not necessarily bot staff.
    "Global Mod": 4,
    "Mod": 4,
    "Subscriber": 2,
    "Pro": 1,
    "User": 1,
    "Muted": 0,
    "Banned": 0
}

with open(path.join(path.dirname(__file__), "emoji.json"),
          encoding="utf-8") as file:
    EMOJI = json.load(file)


def parse_message(packet):
    """Parse a Beam message packet."""

    message = []
    for component in packet["message"]["message"]:
        chunk = {
            "type": component["type"],
            "data": "",
            "text": component["text"]
        }
        if component["type"] == "emoticon":
            chunk["type"] = "emoji"
            chunk["data"] = EMOJI.get(component["text"], "")
            message.append(chunk)
        elif component["type"] == "inaspacesuit":
            chunk["type"] = "emoji"
            chunk["data"] = ""
            message.append(chunk)
        elif component["type"] == "link":
            chunk["type"] = "url"
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
        role=ROLES[packet["user_roles"][0]],
        action=packet["message"]["meta"].get("me", False),
        target=packet["message"]["meta"].get(
            "whisper", None) and packet["target"]
    )


def parse_follow(packet):
    """Parse follow packet."""

    return EventPacket(
        "follow",
        packet["user"]["username"],
        packet["following"]
    )


def parse_subscribe(packet):
    """Parse subscribe packet."""

    return EventPacket("subscribe", packet["user"]["username"])


def parse_resubscribe(packet):
    """Parse resubscribe packet."""

    return EventPacket("subscribe", packet["user"]["username"],
                       streak=packet["totalMonths"])


def parse_host(packet):
    """Parse host packet."""

    return EventPacket("host", packet["hoster"]["token"])


def parse_join(packet):
    """Parse join packet."""

    return EventPacket("join", packet["username"])


def parse_leave(packet):
    """Parse host packet."""

    return EventPacket("leave", packet["username"])


def synthesize(packet):
    """Create a Beam packet from a :obj:`MessagePacket`."""

    message = ""

    if packet.action:
        message = "/me "

    for index, component in enumerate(packet):
        if component.type == "emoji":
            message += EMOJI.get(component.data, component.text)
            if (index < len(packet) - 1 and
                    not packet[index + 1].startswith(' ')):
                message += ' '
        elif component.type == "tag":
            message += '@' + component.data
        else:
            message += component.text

    if packet.target:
        return (packet.target, message), {"method": "whisper"}

    return (message,), {}
