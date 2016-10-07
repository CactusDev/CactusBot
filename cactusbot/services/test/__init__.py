from ..handler import Handler
from ..storage import BeamMessage


class BeamHandler(Handler):
    def __init__(self, data):
        """
        Initialize the generalizer for Beam
        Arguments:
            data - dict of JSON data from Beam
        """
        super().__init__()

        # The handler name, because it's required
        self.NAME = "beam"
        # The action level, 1 acts on the data directly from the source
        self.ACTION = 1
        # Not async, the code in this handler will affect data that other
        # handlers will require
        self.IS_ASYNC = False
        # Data from Beam, in raw JSON
        # Needs to be converted into CB data format
        self.data = data
        # Data to be sent back to Beam, in Beam format
        self.packet = {}

    async def run(self):
        """Runs the handler"""
        # Convert the data into the CB service-agnostic object
        self.packet = await convert_packet()

        # Return that object
        return self.packet

    async def convert_packet(self):
        """Converts the raw Beam packet into the CB service-agnostic object"""

        message = " ".join(
            [obj.get("text", "") for obj in self.data["message"]["message"]])

        obj = BeamMessage(
            self.data,
            self.data["channel"],
            self.data["id"],
            self.data["user_name"],
            self.data["user_id"],
            self.data["user_roles"],
            message
        )

        return obj
