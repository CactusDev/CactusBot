from ...packets import MessagePacket


class BeamParser:

    @classmethod
    def parse_message(cls, packet):
        message = []
        for chunk in packet["message"]["message"]:
            if chunk["type"] == "emoticon":
                # TODO: emoticon map
                message.append({
                    "type": chunk["type"],
                    "data": "unknown",  # HACK
                    "text": chunk["text"]
                })
            elif chunk["type"] == "link":
                message.append({
                    "type": chunk["type"],
                    "data": chunk["url"],
                    "text": chunk["text"]
                })
            elif chunk["type"] == "tag":
                message.append({
                    "type": chunk["type"],
                    "data": chunk["username"],
                    "text": chunk["text"]
                })
            elif chunk["text"]:
                message.append({
                    "type": chunk["type"],
                    "data": chunk["data"],
                    "text": chunk["text"]
                })
        return MessagePacket(*message, user=packet["user_name"])
