"""Handle handlers."""

import logging

from .packets import MessagePacket, Packet


class Handlers(object):
    """Evented controller for individual handlers.

    For a method to have the ability to be used as an event handler, it must
    be prefixed with `on_`, and then followed by the event name.
    This method gets a single argument of packet.

    Packet can be the following types:

    ================= ===============
    Event             Packet Type
    ================= ===============
    `message`         `MessagePacket`
    `follow`          `EventPacket`
    `subscribe`       `EventPacket`
    `host`            `EventPacket`
    `join`            `EventPacket`
    `leave`           `EventPacket`
    `repeat`          `MessagePacket`
    `config`          `Packet`
    `username_update` `Packet`
    ================= ===============

    Other events will be of the packet type `Packet`.

    Parameters
    ----------
    handlers : :obj:`Handler`
        Tuple of handlers that contain events.

    Examples
    --------

    >>> class TestingHandler(Handler):
    ...     async def on_message(self, packet):
    ...         self.logger.info(packet)
    ...
    >>> handlers = Handlers(TestingHandler)
    >>> async def handle():
    ...     await handlers.handle("message", MessagePacket("Message!"))
    ...

    """

    def __init__(self, *handlers):
        self.logger = logging.getLogger(__name__)

        self.handlers = handlers

    async def handle(self, event, packet):
        """Handle incoming data.

        Parameters
        ----------
        event : :obj:`str`
            The event that should be handled
        packet : :obj:`Packet`
            The packet to send to the handler function

        Examples
        --------
        >>> async def handle():
        ...     await handlers.handle("message", MessagePacket("Message!"))
        ...

        """

        result = []

        for handler in self.handlers:
            if hasattr(handler, "on_" + event):
                try:
                    response = await getattr(handler, "on_" + event)(packet)
                except Exception:
                    self.logger.warning(
                        "Exception in handler %s:", type(handler).__name__,
                        exc_info=1)
                else:
                    for packet in self.translate(response, handler):
                        if packet is StopIteration:
                            return result
                        result.append(packet)
                        # TODO: In Python 3.6, with asynchronous generators:
                        # yield packet

        return result

    def translate(self, packet, handler):
        """Translate :obj:`Handler` responses to :obj:`Packet`.

        Parameters
        ----------
        packet : :obj:`Packet` immediately yielded,\
            :obj:`str` converted into a text field in a `MessagePacket`,\
            :obj:`tuple` / :obj:`list` iterated over, yields each item,\
            :obj:`StopIteration` stops packets from being passed, or\
            :obj:`None` an ignored packet
            The packet to turn the handler response into
        handler : :obj:`Handler`
            The handler response to turn into a packet

        Examples
        --------
        >>> class TestingHandler(Handler):
        ...     async def on_message(self, packet):
        ...         self.logger.info(packet)
        ...
        >>> handlers = Handlers(TestingHandler)
        >>> packet = MessagePacket("Testing!")
        >>> async def handle():
        ...     await handlers.handle("message", MessagePacket("Message!"))
        ...     handlers.translate(packet, TestingHandler)
        ...

        """

        if isinstance(packet, Packet):
            yield packet
        elif isinstance(packet, (tuple, list)):
            for component in packet:
                yield from self.translate(component, handler)
        elif isinstance(packet, str):
            yield MessagePacket(packet)
        elif packet is StopIteration:
            yield packet
        elif packet is None:
            pass
        else:
            self.logger.warning("Invalid return type from %s: %s",
                                type(handler).__name__, type(packet).__name__)


class Handler(object):
    """Parent class to all event handlers.

    Examples
    --------
    >>> class TestingHandler:
    ...     def on_message(self, packet):
    ...         self.logger.info(packet)
    ...

    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
