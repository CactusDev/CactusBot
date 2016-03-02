from json import load, loads, dumps
from time import strftime, sleep
import statistics

import asyncio
import websockets


def message_handler(parent, data):
    user = data['user_name']
    statistics.add_total_message(user)

    # print(data)
    msg = data["message"]["message"]
    message = ""
    # Iterate through the message,
    # so we can get text from emoticons & links
    for i in range(0, len(msg)):
        if msg[i]["type"] in ("emoticon", "link"):
            message += msg[i]["text"]
        else:
            message += msg[i]["data"]

    parent.logger.info("[{usr}] {msg}".format(usr=user, msg=message))

    return None


def join_handler(parent, data):
    username = data['username']

    statistics.add_total_view(username)

    parent.logger.info("[{room}][{rid}] {user} joined".format(user=username,
                                                              room=parent.channel_data["token"],
                                                              rid=parent.channel_data["id"]))

    if parent.config["announce_enter"]:
        parent.send_message("Welcome {username}".format(username=data["username"]))


def leave_handler(parent, data):

    parent.logger.info("[{room}][{rid}] {user} left".format(user=data["username"],
                                                            room=parent.channel_data["token"],
                                                            rid=parent.channel_data["id"]))

    if parent.config["announce_leave"]:
        parent.send_message("See you {username}".format(username=data["username"]))


def check_spam(self, message, is_mod):
    with open('data/config.json') as f:
        config = load(f)
        max_cap = config['max_caps']
        cap = 0
        msg = message.replace(' ', '')
        pos = 0

        for char in message:
            if not is_mod:
                for char in msg:
                    if any(char.isupper()):

                        if cap >= max_cap:
                            break
                            return True
                        elif cap < max_cap and pos is len(msg):
                            break
                            return False

                        cap += 1
                        pos += 1
