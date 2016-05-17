# TODO: metaclass, to run function after service handler and send


class Handler:

    @staticmethod
    def on_message(message):
        return "Echo! {}".format(message)

    # @staticmethod
    # def on_command(message):
    #     return "Yay, a command!"

    @staticmethod
    def on_join(user):
        # self.logger.info("- {user} joined".format(
        #     user=data["username"]))
        #
        # if self.config.get("announce_enter", False):
        #     self.send_message("Welcome, @{username}!".format(
        #         username=data["username"]))
        return "Welcome, {}!".format(user)

    @staticmethod
    def on_leave(user):
        # if data["username"] is not None:
        #     self.logger.info("- {user} left".format(
        #         user=data["username"]))
        #
        #     if self.config.get("announce_leave", False):
        #         self.send_message("See you, @{username}!".format(
        #             username=data["username"]))
        return "Goodbye, {}.".format(user)
