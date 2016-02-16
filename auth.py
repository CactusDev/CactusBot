
from requests import Session
import cactusBot

channelID = 0
botName = ""
botPassword = ""

def login(username, password):
    color("Trying to login...", colors.OTHER)

    auth = {
        "username": username,
        "password": password
        }

    if not "channel" in cactusBot.channelData:
        raise AuthenticationException("Incorrect username and / or password")

    return session.post(path + "/users/login", auth).json()

def loadConfig():
    pass
