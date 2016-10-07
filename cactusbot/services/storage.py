class Storage(object):
    """
    Stores the information about a message from a service in a service-agnostic
    format.

    Message is a parent object for all forms of packets
    """
    # Default type is a message
    TYPE = "message"
    # Default service is Beam
    SERVICE = "beam"
    # raw is the raw data from the service
    # (JSON from Beam, whatever that abomination Twitch uses is called)
    raw = None

    def export(self):
        """
        When implemented, should return the service-specific format in dict
            form
        """
        return NotImplementedError

    def send(self):
        """
        When implemented, will return an asyncio coroutine to be called later
            that sends the response to the appropriate service
        """
        return NotImplementedError


class BeamMessage(Storage):
    def __init__(self, raw, channel, msg_id, user_name, user_id, user_roles,
                 message):
        self.raw = raw
        self.TYPE = "message"
        self.SERVICE = "beam"
        self.channel = channel
        self.msg_id = msg_id
        self.user_name = user_name
        self.user_id = user_id
        self.user_roles = user_roles
        self.message = message

        super().__init__()

    def export(self):
        """Returns the service-specific format in dict form"""
        # ID is the initializing message ID +1
        return {
            "type": "method",
            "method": "msg",
            "arguments": [
                self.message
            ],
            "id": self.msg_id + 1
        }

    def send(self):
        """
        Returns an asyncio coroutine to be called later
        """
        return beam_send

    async def beam_send(self):
        """Send the response to Beam"""
        pass


class BeamSub(Storage):
    def __init__(self, data):
        self.raw = data
        self.TYPE = "subscription"
        self.SERVICE = "beam"

        super().__init__()

    def export(self):
        """Returns the service-specific format in dict form"""
        pass

    def send(self):
        """
        Returns an asyncio coroutine to be called later
        """
        return export_send

    async def beam_send(self):
        """Send the response to Beam"""
