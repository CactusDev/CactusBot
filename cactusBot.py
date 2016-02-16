
from requests import Session
import json
import os

from exception import AuthenticationException

from color import *

session = Session()

startTime = 0
loadTime = 0

path = "https://beam.pro/api/v1"


def login(username, password):
    color("Trying to login...", colors.OTHER)

    auth = {
        "username": username,
        "password": password
    }

    channelData = login(auth.get('username'), auth.get('password'))
    if "channel" not in channelData:
        raise AuthenticationException("Incorrect username and / or password")

    return session.post(path + "/users/login", auth).json()


def init():
    if not os.path.exists('data/bot.json'):
        out.err("The config file doesn't exist! Please run \'setup.py\' first")
    else:
        log("Config file found.", colors.OTHER)

        with open('data/bot.json') as data:
            data = json.load(data)

            channelID = data.get('connectTo')
            botName = data.get('botName')
            botPassword = data.get('botPassword')

        log("Logged in as: {user}!".format(user=botName), colors.OTHER)
init()
