class CacheUtils(object):

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def in_cache_followers(user):
        """ Returns if user is in the cache. """
        follower_cache = open("caches/CacheFollowers.txt", "r")
        for line in follower_cache:
            if user in line:
                follower_cache.close()
                return True
        follower_cache.close()
        return False

    def cache_followers_add(user):
        """ Adds user to cache with newline at end. """
        follower_cache = open("caches/CacheFollowers.txt", "a+")
        follower_cache.write(user + "\n")
        follower_cache.close()
