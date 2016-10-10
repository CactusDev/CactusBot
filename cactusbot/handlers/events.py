"""Handle events"""

from ..handler import Handler
from ..packets import MessagePacket
from ..cached import CacheUtils
import time
import calendar


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_data):
        super().__init__()

        self.cache_follows = cache_data["CACHE_FOLLOWS"]
        self.cache_follows_time = cache_data["CACHE_FOLLOWS_TIME"]

    def on_follow(self, packet):
        """Handle follow packets."""
        def on_follow_return():
            # TODO: Make configurable
            return MessagePacket(
                "Thanks for following, @{} !".format(packet.user)
            )

        if packet.success:
            if self.cache_follows:
                cache = CacheUtils("caches/followers.json")
                if cache.in_cache(packet.user):
                    if self.cache_follows_time > 0:
                        configtime = int(self.cache_follows_time * 60)
                        cache_time = int(calendar.timegm(tuple(
                                    cache.return_data(packet.user))))

                        if (cache_time + configtime) <= int(time.time()):
                            cache.cache_add(packet.user)
                            return on_follow_return()
                        else:
                            cache.cache_add(packet.user)
                else:
                    cache.cache_add(packet.user)
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
