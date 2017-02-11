"""Event packet."""

from .packet import Packet


class EventPacket(Packet):
    """Packet to store events.

    Parameters
    ----------
    event_type : :obj:`str`
        Event type.
    user : :obj:`str`
        User identifier.
    success : :obj:`bool`
        Whether or not the event was positive or successful.
    """

    def __init__(self, event_type, user, success=True, streak=1):
        super().__init__()

        self.event_type = event_type
        self.user = user
        self.success = success
        self.streak = streak

    def __str__(self):
        return "<Event: {} - {}>".format(self.user, self.event_type)

    @property
    def json(self):
        """JSON representation of the packet.

        Returns
        -------
        :obj:`dict`
            Object attributes, in a JSON-compatible format.

        Examples
        --------
        >>> import pprint
        >>> pprint.pprint(EventPacket("follow", "Stanley").json)
        {'event': 'follow', 'success': True, 'user': 'Stanley'}
        """
        return {
            "user": self.user,
            "event": self.event_type,
            "success": self.success,
            "streak": self.streak
        }
