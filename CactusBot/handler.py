# TODO: metaclass, to run function after service handler and send
# TODO: @config("value") decorator


class Handler:

    def __init__(self, *args, **kwargs):
        self.send = self.send or print

    async def on_message(self, message):
        await self.send("Echo! {}".format(message))

    # @staticmethod
    # def on_command(message):
    #     return "Yay, a command!"

    async def on_join(self, user):
        # self.logger.info("- {user} joined".format(
        #     user=data["username"]))
        #
        # if self.config.get("announce_enter", False):
        #     self.send_message("Welcome, @{username}!".format(
        #         username=data["username"]))
        await self.send("Welcome, {}!".format(user))

    async def on_leave(self, user):
        # if data["username"] is not None:
        #     self.logger.info("- {user} left".format(
        #         user=data["username"]))
        #
        #     if self.config.get("announce_leave", False):
        #         self.send_message("See you, @{username}!".format(
        #             username=data["username"]))
        await self.send("Goodbye, {}.".format(user))
