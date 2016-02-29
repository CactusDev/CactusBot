from json import load, loads, dumps
from time import strftime, sleep

import asyncio
import websockets


def message_handler(parent, data):
    # print(data)
    msg = data["message"]["message"]
    message = ""
    # Iterate through the message,
    # so we can get text from emoticons & links
    for i in range(0, len(msg)):
        print(msg[i])
        if msg[i]["type"] in ("emoticon", "link"):
            message += msg[i]["text"]
        else:
            message += msg[i]["data"]

    user = data["user_name"]
    parent.logger.info("[{usr}] {msg}".format(usr=user, msg=message))

    return None


def join_handler(parent, data):
    parent.logger.info("[{room}][{rid}] {user} joined".format(user=data["username"],
                                                              room=parent.channel_data["token"],
                                                              rid=parent.channel_data["id"]))

    if parent.config["announce_enter"]:
        parent.logger.warn("THIS ISN'T SENDING A MESSAGE")
        print(type(parent.send_message("")), repr(parent.send_message("")))
        parent.send_message("Welcome {username}".format(username=data["username"]))


def leave_handler(parent, data):
    parent.logger.info("[{room}][{rid}] {user} left".format(user=data["username"],
                                                            room=parent.channel_data["token"],
                                                            rid=parent.channel_data["id"]))

    if parent.config["announce_leave"]:
        parent.logger.warn("THIS ISN'T SENDING A MESSAGE")
        parent.send_message("See you {username}".format(username=data["username"]))
