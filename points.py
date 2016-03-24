from json import load
from models import PtsCmd


class Points:

    def give_points():
        per_int = 0
        interval = 0

        with open('data/config.json') as f:
            data = load(f)

            per_int = data['points']['points_per_interval']
            interval = data['points']['interval']

        count_time = interval * 60

        for i in range(count_time):
            i -= 1
