"""Follower caching."""

import datetime
import json


class CacheUtils:
    """Follower caching."""

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, encoding="utf-8") as file:
            cache = json.load(file)
        return cache.__iter__()

    def __getitem__(self, user):
        with open(self.filename, encoding="utf-8") as file:
            cache = json.load(file)
        return datetime.datetime.strptime(cache[user], "%Y-%m-%dT%H:%M:%S.%f")

    def __setitem__(self, user, value):
        with open(self.filename, encoding="utf-8") as file:
            cache = json.load(file)
        cache[user] = value
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(cache, file, indent=2)
