"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket
from ..cached import CacheUtils


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_follows):
        super().__init__()

        self.cache_follows = cache_follows

    def on_follow(self, packet):
        """Handle follow packets."""
        def on_follow_return():
            # TODO: Make configurable
            return MessagePacket(
                "Thanks for following, @{} !".format(packet.user)
            )

        if packet.success:
            if self.cache_follows:
                if not(CacheUtils.in_cache_followers(packet.user)):
                    CacheUtils.cache_followers_add(packet.user)
                    return on_follow_return()
            else:
                return on_follow_return()

    def on_subscribe(self, packet):
        """Handle subscription packets."""
        # TODO: Make configurable
        return MessagePacket(
            "Thanks for subscribing, @{} !".format(packet.user)
        )

    def on_host(self, packet):
        """Handle host packets."""
        # TODO: Make configurable
        return MessagePacket("Thanks for hosting, @{} !".format(packet.user))
