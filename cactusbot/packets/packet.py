"""Base packet."""

import json


class Packet:
    """Base packet.

    May be used for packets which only require static attributes.

    Parameters
    ----------
    packet_type : :obj:`str` or :obj:`None`
        The name for the packet type. If not specified, the class name is used.
    **kwargs
        Packet attributes.
    """

    def __init__(self, packet_type=None, **kwargs):
        self.type = packet_type or type(self).__name__
        self.kwargs = kwargs

    def __repr__(self):
        return '<{}: {}>'.format(self.type, json.dumps(self.json))

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
        >>> pprint.pprint(Packet(key="key", value="value").json)
        {'key': 'key', 'value': 'value'}
        """
        return self.kwargs
