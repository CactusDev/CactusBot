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
        packet : :obj:`Packet`, :obj:`str`, :obj:`tuple`, :obj:`list`, :exc:`S\
topIteration`, or :obj:`None`
            The packet to turn the handler response into
             - :obj:`Packet` is immediately yielded.
             - :obj:`str` is converted into a text field in a
               :obj:`MessagePacket`.
             - :obj:`tuple` or :obj:`list` is iterated over, passing each
               item through :meth:`translate` again.
             - :exc:`StopIteration` signifies that no future packets should be
               yielded, stopping the chain.
             - :obj:`None` is ignored, and is never yielded.
        handler : :obj:`Handler`
            The handler response to turn into a packet

        Examples
        --------
        >>> handlers = Handlers()
        >>> translated = handlers.translate("Hello!", Handler())
        >>> [(item.__class__.__name__, item.text) for item in translated]
        [('MessagePacket', 'Hello!')]

        >>> handlers = Handlers()
        >>> translated = handlers.translate(["Potato?", "Potato!"], Handler())
        >>> [(item.__class__.__name__, item.text) for item in translated]
        [('MessagePacket', 'Potato?'), ('MessagePacket', 'Potato!')]

        >>> handlers = Handlers()
        >>> translated = handlers.translate(
        ...     ["Stop spamming.", StopIteration, "Nice message!"],
        ...     Handler()
        ... )
        >>> [(item.__class__.__name__, item.text) for item in translated]
        [('MessagePacket', 'Stop spamming.')]
        """

        if isinstance(packet, Packet):
            yield packet
        elif isinstance(packet, (tuple, list)):
            for component in packet:
                for item in self.translate(component, handler):
                    if item is StopIteration:
                        return item
                    yield item
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
