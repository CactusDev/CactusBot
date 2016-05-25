# TODO: metaclass, to run function after service handler and send
# TODO: @config("value") decorator

from logging import getLogger


class Handler(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = getLogger(__name__)

        self.commands = {  # TODO: make dynamic (and less silly)
            "cactus": "Ohai! I'm CactusBot. :cactus",
            "test": "Test confirmed. :cactus",
            "help": "Check out my documentation at cactusbot.readthedocs.org."
        }

    async def send(self, *args, **kwargs):
        self.logger.info(
            "SEND: {args} {kwargs}", dict(args=args, kwargs=kwargs), style='{'
        )

    async def on_message(self, message, user):  # TODO: optimize
        self.logger.info(
            "[%(user)s] %(message)s",
            dict(user=user, message=message)
        )

        # TODO: better command parsing
        if message.startswith('!') and len(message) > 1:
            args = message.split()

            if args[0][1:] in self.commands:
                response = self.commands[args[0][1:]]
            else:
                response = "Command not found."

            await self.send(response)

        # TODO: /cry
        # TODO: spam protection

    async def on_join(self, user):
        self.logger.info("- {} joined".format(user))
        return  # TODO: real fix for delurking
        await self.send("Welcome, @{}!".format(user))

    async def on_leave(self, user):
        self.logger.info("- {} left".format(user))
        return  # TODO: real fix for delurking
        await self.send("Goodbye, @{}.".format(user))
