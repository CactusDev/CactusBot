"""Ban packet."""

from .packet import Packet


class BanPacket(Packet):
    """Packet to store bans.

    Parameters
    ----------
    user : :obj:`str`
        User identifier.
    duration : :obj:`int`, optional
        The length of time for which the ban lasts, in seconds.

        If set to ``0``, the ban lasts for an unlimited amount of time.
    """

    def __init__(self, user, duration=0):
        super().__init__()

        self.user = user
        self.duration = duration

    def __str__(self):
        if self.duration:
            return "<Ban: {}, {} seconds>".format(self.user, self.duration)
        return "<Ban: {}>".format(self.user)

    @property
    def json(self):
        """JSON representation of the packet.

        Returns
        -------
        :obj:`dict`
            Object attributes, in a JSON-compatible format.

        Examples
        --------
        >>> pprint.pprint(BanPacket("Stanley", 60).json)
        {'duration': 60, 'user': 'Stanley'}
        """
        return {
            "user": self.user,
            "duration": self.duration
        }
