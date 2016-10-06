from ...packets import MessagePacket
from . import emotes


class BeamParser:

    @classmethod
    def parse_message(cls, packet):
        message = []
        for chunk in packet["message"]["message"]:
            packet = {
                "type": chunk["type"],
                "data": None,
                "text": chunk["text"]
            }
            if chunk["type"] == "emoticon":
                packet["data"] = emotes.get(chunk["text"], chunk["text"])
                message.append(packet)
            elif chunk["type"] == "link":
                packet["data"] = chunk["url"]
                message.append(packet)
            elif chunk["type"] == "tag":
                packet["data"] = chunk["username"]
                message.append(packet)
            elif chunk["text"]:
                packet["data"] = chunk["data"]
                message.append(packet)

        return MessagePacket(*message, user=packet["user_name"])
