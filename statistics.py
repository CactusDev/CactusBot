
from json import load, dump, loads, dumps


class Statistics:

    messages = 0
    polls = 0
    deleted_messages = 0
    parsed = ""

    def recv(self, data):
        parsed = loads(data)
        where = parsed['location']

        if where == "live":
            val = self.get('average-viewers')
            val += parsed['AverageViewers'] / 2
            self.write('average-viewers', val)

            val = self.get('total-resubs')
            self.write('total-resubs', (parsed['Resubs'] + val))

            val = self.get("total-subs")
            val += parsed['Subs']
            self.write('total-subs', parsed['Subs'])

            val = self.get('total-followers')
            val += parsed['Follows']
            self.write('total-followers', val)

            val = self.get('total-unfollows')
            val += self.parsed['Unfollows']
            self.write('total-unfollows', val)
        elif where == "close":
            val = self.get('total-messages')
            val += parsed['Messages']
            self.write('total-messages', val)

            val = self.get('polls')
            val += parsed['Polls']
            self.write('total-polls', val)

            val = self.get('deleted-messages')
            val += parsed['Deleted']
            self.write('deleted-messages', val)

            val = self.get('commands-run')
            val += parsed['Commands']
            self.write('commands-run', val)

            val = self.get('total-views')
            val += parsed['Views']
            self.write('total-views', val)
        else:
            raise Exception("{} is not a known location".format(where))

    def get(self, location):
        with open('data/stats.json', 'r') as f:
            f = load(f)

            try:
                return f[location]
            except:
                raise Exception("{} is not in the stats file".format(location))

    def write(self, location, data):
        with open('data/stats.json', 'w', encoding='utf-8') as f:
            stats = load(f)

            stats[location] = data

            dump(stats, f, indent=4, skipkeys=False, sort_keys=True)

stat = Statistics()

data = {
    "location": "close",
    "Views": 100,
    "Deleted": 1000,
    "Commands": 1000,
    "Messages": 100000,
    "Polls": 10
}

print(data)

stat.recv(dumps(data))
