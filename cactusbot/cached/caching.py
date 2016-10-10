import json
import time


class CacheUtils(object):

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def __init__(self, cacheName):
        super().__init__()

        self.cacheName = cacheName

    def in_cache(self, user):
        """ Returns if user is in the cache, and if so, the time in secs """
        with open(self.cacheName) as cache:
            cachedata = json.load(cache)
        if user in cachedata.keys():
            return True
        return False

    def cache_add(self, user):
        """ Adds user to cache with newline at end. """
        with open(self.cacheName, "r") as cache:
            cachedata = json.load(cache)
        cachedata[user] = time.gmtime()
        with open(self.cacheName, "w") as cache:
            json.dump(cachedata, cache, indent=4)

    def return_data(self, user):
        with open(self.cacheName) as cache:
            cachedata = json.load(cache)
            return cachedata[user]
