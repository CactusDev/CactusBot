
import asyncio
import requests
from time import sleep
from json import load
import sqlite3 as sql


class Points():

    @asyncio.coroutine
    def auto_points(self, channel):
        global active

        while True:
            with requests.Session() as session:
                users = session.get(self.path + '/chats/{id}/users'.format(
                    id=channel))

            users = users.json()

            config = load(open('data/config.json'))
            interval = config['interval']
            per_interval = config['points_per_interval']

            for user in users:
                username = user['userName']
                self.add_points(username, per_interval)

            sleep(float(interval)*60)

    def add_points(self, user, amt):
        conn = sql.connect("data/bot.db")
        c = conn.cursor()

        old = int(c.execute('''SELECT points FROM points WHERE username={user}'''.format(user=user)))

        c.execute('''UPDATE points SET points={new} WHERE username={user}'''.format(
            new=old + amt))

        conn.execute()
        conn.close()

    def set_points(self, user, amt):
        conn = sql.connect('data/bot.db')
        c = conn.cursor()

        c.execute('''UPDATE points SET points={new} WHERE username={user}'''.format(
            new=amt, user=user))

        conn.commit()
        conn.close()

    def get_points(self, user):
        conn = sql.connect('data/bot.db')
        c = conn.cursor()

        points = c.execute('''SELECT points FROM points WHERE username={user}'''.format(
            user=user))

        return int(points)
