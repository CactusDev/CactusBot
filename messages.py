from user import User


class MessageHandler(User):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self.config = {}

    def handle(self, response):
        if "event" in response:
            events = {
                "ChatMessage": self.message_handler,
                "UserJoin": self.join_handler,
                "UserLeave": self.leave_handler
            }

            if response["event"] in events:
                events[response["event"]](response["data"])
            else:
                pass
                self.logger.debug("No function found for event {}.".format(
                    response["event"]
                ))

    def message_handler(self, data):
        message = data["message"]["message"]
        parsed = str()
        for chunk in message:
            if chunk["type"] == "text":
                parsed += chunk["data"]
            else:
                parsed += chunk["text"]

        user = data["user_name"]
        self.logger.info("[{user}] {message}".format(
            user=user, message=parsed))

    def join_handler(self, data):
        self.logger.info("[[{channel}]] {user} joined".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_enter", False):
            yield from self.send_message("Welcome, {username}!".format(
                username=data["username"]))

    def leave_handler(self, data):
        self.logger.info("[[{channel}]] {user} left".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_leave", False):
            yield from self.send_message("See you, {username}!".format(
                username=data["username"]))
