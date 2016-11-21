import inspect
from collections import defaultdict
from functools import wraps

import requests


# http://stackoverflow.com/a/25959545/6119465
def get_owner_class(meth):
    return getattr(inspect.getmodule(meth),
                   meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])


def service(name=None):

    def decorator(function):

        owner = get_owner_class(function)
        owner._map[function.__name__][name] = function

        @wraps(function)
        def wrapped(self, service=None, *args, **kwargs):

            function_map = owner._map[function.__name__]
            return function_map[service](*args, **kwargs)

        return wrapped

    return decorator


class Base:
    _map = defaultdict(dict)

########


# Weird, but annoyingly required:


class Test(Base):
    pass


class Test(Base):

    @service("beam")
    def test():
        return "BEAM TEST \o/"

    @service("discord")
    def test():
        return "DISCORD TEST (>^.^)>"

    @service()
    def test():
        return "General test! :D"

    @service("beam")
    def get_title(channel):
        return requests.get(
            "https://beam.pro/api/v1/channels/" + channel
        ).json()["name"]

    @service("twitch")
    def get_title(channel, client_id):
        return requests.get(
            "https://api.twitch.tv/kraken/channels/" + channel,
            headers={"client-id": client_id}
        ).json()["status"]
