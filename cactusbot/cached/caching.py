import json
import dateutil.parser


class CacheUtils:

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename) as file:
            cache = json.load(file)
        return cache.__iter__()

    def __getitem__(self, user):
        with open(self.filename) as file:
            cache = json.load(file)
        return dateutil.parser.parse(cache[user])

    def __setitem__(self, user, value):
        with open(self.filename) as file:
            cache = json.load(file)
        cache[user] = value
        with open(self.filename, 'w') as file:
            json.dump(cache, file, indent=2)
