from user import User
from models import Command, session, CommandCommand, QuoteCommand, CubeCommand, SocialCommand, ScheduleCommand
from asyncio import async, coroutine
from functools import partial


class MessageHandler(User):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def handle(self, response):
        if "event" in response:
            events = {
                "ChatMessage": self.message_handler,
                "UserJoin": self.join_handler,
                "UserLeave": self.leave_handler
            }

            if response["event"] in events:
                async(coroutine(
                    partial(events[response["event"]], response["data"])
                )())
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

        if parsed[0].startswith("!") and len(parsed) > 1:
            args = parsed.split()

            commands = {
                "command": CommandCommand,
                "quote": QuoteCommand,
                "cube": CubeCommand,
                "social": SocialCommand,
                "schedule": ScheduleCommand,
            }
            if args[0][1:] in commands:
                yield from self.send_message(
                    commands[args[0][1:]]()(args, data))
            else:
                command = session.query(
                    Command).filter_by(command=args[0][1:]).first()
                if command:
                    response = command(user, *args)
                    yield from self.send_message(response)
                else:
                    yield from self.send_message("Command not found.")

    def join_handler(self, data):
        self.logger.info("[[{channel}]] {user} joined".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_enter", False):
            yield from self.send_message("Welcome, @{username}!".format(
                username=data["username"]))

    def leave_handler(self, data):
        self.logger.info("[[{channel}]] {user} left".format(
            channel=self.channel_data["token"], user=data["username"]))

        if self.config.get("announce_leave", False):
            yield from self.send_message("See you, @{username}!".format(
                username=data["username"]))
