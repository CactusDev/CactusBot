
from os.path import exists
from shutil import copy
from json import loads

class Statistics:

    def __init__(self):
        self.logger.info("Starting statistics engine.")

        if exists('data/stats.json'):
            self.logger.info("Found statistics file.")
        else:
            self.logger.info("Statistics file not found. Creating.")
            copy('data/stats-template.json')
            self.logger.info("Created!")

        self.logger.info("Started statistics engine.")


    def add_resub(self, username):
        with open('data/stats.json') as stats:
            stats = loads(stats)
            cur_resubs = int(stats['total-resubs'])
            stats['total-resubs'] = cur_resubs + 1
            stats.close()

    def add_sub(self, username):
            with open('data/stats.json') as stats:
                stats = loads(stats)
                cur_subs = int(stats['total-subs'])
                stats['total-subs'] = cur_subs + 1
                stats.close()

    def add_follower(self, username):
            with open('data/stats.json') as stats:
                stats = loads(stats)
                cur_followers = int(stats['total-followers'])
                stats['total-followers'] = cur_followers + 1
                stats.close()

    def add_total_message(self, username):
            with open('data/stats.json') as stats:
                stats = loads(stats)
                cur_messages = int(stats['total-messages'])
                stats['total-messages'] = cur_messages + 1
                stats.close()

    def add_total_view(self, username):
            with open('data/stats.json') as stats:
                stats = loads(stats)
                cur_views = int(stats['total-views'])
                stats['total-views'] = cur_views + 1
                stats.close()

    def add_unique_viewer(self, username):
        with open('data/stats.json') as stats:
            stats = loads(stats)
            curr_unique = int(stats['unique-views'])
            stats['unique-views'] = curr_unique + 1
            stats.close()
