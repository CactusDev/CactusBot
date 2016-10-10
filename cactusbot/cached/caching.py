class CacheUtils(object):

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def in_cache_followers(user):
        """ Returns if user is in the cache. """
        follower_cache = open("Caches/CacheFollowers.txt", "r")

        final = False
        for line in follower_cache:
            if user in line:
                final = True
        follower_cache.close()
        return final

    def cache_followers_add(user):
        """ Adds user to cache with newline. """
        follower_cache = open("Caches/CacheFollowers.txt", "a+")
        follower_cache.write(user + "\n")
        follower_cache.close()
