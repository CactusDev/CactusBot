from user import User
from models import Command, CommandFactory, session
from asyncio import async, coroutine
from functools import partial
from re import sub


class MessageHandler(User):
    roles = {
        "moderator": ("Owner", "Staff", "Founder", "Global Mod", "Mod"),
        "standard": ("Subscriber", "Pro", "User"),
        "ignored": ("Muted", "Banned")
    }
    factory = CommandFactory()

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

        if parsed.startswith("!"):
            async(self.command_parser(data, parsed))

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

    def command_parser(self, data, message):
        response = data

        role = data["user_roles"][0]
        user = data['user_name']

        # This is very bad and will change soon! Entirely temporary.
        split = message[1:].split()
        if split[0] == "command":
            if role in self.roles["moderator"]:
                if len(split) > 2:
                    if split[1] in ("add", "remove"):
                        if split[1] == "add":
                            self.factory.add_command(split[2], ' '.join(
                                split[3:]), response["user_id"])
                            yield from self.send_message(
                                "Added command !{}.".format(split[2]))
                        elif split[1] == "remove":
                            self.factory.remove_command(split[2])
                            yield from self.send_message(
                                "Removed command !{}.".format(split[2]))
                else:
                    yield from self.send_message("Not enough arguments!")
            else:
                yield from self.send_message("!command is moderator-only.")
        elif split[0] == "murdilate" and role in self.roles["moderator"]:
            raise exit("Murdilated.")
        else:
            command = self.factory.session.query(
                Command).filter_by(command=split[0]).first()
            if command:
                command.calls += 1
                session.commit()

                response = command.response

                response = response.replace("%name%", user)
                response = sub(
                    "%arg(\d+)%",
                    lambda m: split[int(m.groups()[0])],
                    response
                )
                response = response.replace("%args%", ' '.join(split[1:]))
                response = response.replace("%count%", str(command.calls))

                yield from self.send_message(response)
            else:
                yield from self.send_message("Command not found.")
