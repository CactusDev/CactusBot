# TODO: metaclass, to run function after service handler and send
# TODO: @config("value") decorator

from logging import getLogger

from .api import CactusAPI
from .commands import commands

from uuid import uuid4
from base64 import b32encode
from traceback import format_exc


class Handler(object):

    def __init__(self):

        self.logger = getLogger(__name__)

        api = CactusAPI(None)  # FIXME: pass correct user

        self.commands = {
            "cactus": "Ohai! I'm CactusBot. :cactus",
            "test": "Test confirmed. :cactus",
            "help": "Check out my documentation at cactusbot.readthedocs.org."
        }

        self.commands.update(
            dict((command.__command__, command(api)) for command in commands)
        )

    async def send(self, *args, **kwargs):
        raise NotImplementedError

    async def on_message(self, message, user):
        message = message.strip()

        self.logger.info("[%s] %s", user, message)

        if message.startswith('!') and len(message) > 1:
            args = message.split()
            command = args.pop(0)[1:]

            if command in self.commands:
                response = self.commands[command]
                if callable(response):
                    try:
                        response = await response(*args)
                    except Exception:
                        code = b32encode(uuid4().bytes).decode()[:12]
                        traceback = format_exc()
                        self.logger.error("Code: %s\n%s", code, traceback)
                        return ("An error occured. Please send code {} to "
                                "CactusDev.").format(code)
            else:
                response = "Command not found."

            return response

        # TODO: spam protection

    async def on_join(self, user):
        self.logger.info("- %s joined", user)
        return "Welcome, @{}!".format(user)

    async def on_leave(self, user):
        self.logger.info("- %s left", user)
        return "Goodbye, @{}.".format(user)

    async def on_follow(self, user):
        self.logger.info("- %s followed", user)
        return "Thanks for the follow, @{}!".format(user)

    async def on_subscribe(self, user):
        self.logger.info("- %s subscribed", user)
        return "Thanks for the subscription, @{}!".format(user)
