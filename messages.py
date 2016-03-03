from user import User
from models import Command, CommandFactory
from asyncio import async, coroutine


class MessageHandler(User):

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    @coroutine
    def handle(self, response):
        if "event" in response:
            events = {
                "ChatMessage": self.message_handler,
                # "UserJoin": self.join_handler,
                # "UserLeave": self.leave_handler
            }
            async(coroutine(self.message_handler))

            if response["event"] in events:
                print(":3")
                async(coroutine(events[response["event"]](response["data"])))
            else:
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

        user = data.get("user_name", "[Beam]")
        self.logger.info("[{user}] {message}".format(
            user=user, message=parsed))

        if parsed.startswith("!"):
            async(coroutine(self.command_parser(data, parsed)))

    # @coroutine
    def join_handler(self, data):
        self.logger.info("[[{channel}]] {user} joined".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_enter", True):
            yield from self.send_message("Welcome, {username}!".format(
                username=data["username"]))

    # @coroutine
    def leave_handler(self, data):
        self.logger.info("[[{channel}]] {user} left".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_leave", False):
            yield from self.send_message("See you, {username}!".format(
                username=data["username"]))

    def command_parser(self, data, message):
        response = data

        # This is very bad and will change soon! Entirely temporary.
        if message.startswith('!'):
            split = message.split()
            if split[0][1:] == "command" and split[1] == "add" and len(split) > 3:
                if any((role in response["user_roles"] for role in ("Owner", "Mod"))):
                    CommandFactory.add_command(self, split[2], ' '.join(
                        split[3:]), response["user_id"])
                    yield from self.send_message("Added command !{}.".format(split[2]))
                else:
                    yield from self.send_message("Mod-only! GRAWR")
            elif split[0][1:] == "command" and split[1] == "rm" and len(split) > 2:
                if any((role in response["data"]["user_roles"] for role in ("Owner", "Mod"))):
                    CommandFactory.remove_command(self, split[2])
                    yield from self.send_message("Removed command !{}.".format(split[2]))
                else:
                    yield from self.send_message("Mod-only! GRAWR")
            elif split[0][1:] == 'murdilate':
                raise KeyboardInterrupt("Murdilated.")
            else:
                q = CommandFactory.session.query(
                    Command).filter_by(command=split[0][1:]).first()
                if q:
                    yield from self.send_message(q.response)
                else:
                    yield from self.send_message("Command not found.")
