
from json import load, dump


class Statistics:

    messages = 0
    polls = 0
    deleted_messages = 0

    def close(self):
        self.write('total-messages', self.messages)

    def recv(self, data):
        pass

    def write(self, location, data):
        with open('data/stats.json') as f:
            stats = load(f)

            stats[location] = data

            dump(f, data, indent=4, sort_keys=True)
