
from os.path import exists
from shutil import copy
from json import load, dump


def __init__(self):
    self.logger.info("Starting statistics engine.")
    if exists('data/stats.json'):
        self.logger.info("Found statistics file.")
    else:
        self.logger.info("Statistics file not found. Creating.")
        copy('data/stats-template.json')
        self.logger.info("Created!")

    self.logger.info("Started statistics engine.")


def add_resub(username):
    with open('data/stats.json') as f:
        stats = load(f)
        stats['total-resubs'] += 1
        dump(stats, f)


def add_sub(username):
        with open('data/stats.json') as f:
            stats = load(f)
            stats['total-subs'] += 1
            dump(stats, f)


def add_follower(username):
        with open('data/stats.json') as f:
            stats = load(f)
            stats['total-followers'] += 1
            dump(stats, f)


def add_total_message(username):
        with open('data/stats.json') as f:
            stats = load(f)
            stats['total-followers'] += 1
            dump(stats, f)


def add_total_view(username):
        with open('data/stats.json') as f:
            stats = load(f)
            stats['total-views'] += 1
            dump(stats, f)


def add_unique_viewer(username):
    with open('data/stats.json') as f:
        stats = load(f)
        stats['unique-views'] += 1
        dump(stats, f)


def add_deleted_message(username):



def add_banned_user(username):
    with open('data/stats.json') as f:
        stats = load(f)
        stats['total-banned-users'] += 1
        dump(stats, f)
