from logging import getLogger as get_logger
# from ..commands import (CommandCommand, QuoteCommand, CubeCommand,
#                         SocialCommand, UptimeCommand, PointsCommand,
#                         TemmieCommand, FriendCommand, SpamProtCommand,
#                         ProCommand, SubCommand, RepeatCommand)
from ..models import session, User, Command

# from re import findall

from ..handler import Handler


class BeamHandler(Handler):

    def __init__(self, *args, **kwargs):
        super(BeamHandler, self).__init__(*args, **kwargs)
        self.logger = kwargs.get("logger") or get_logger(__name__)
        self.events = {
            "ChatMessage": self.on_message,
            "UserJoin": self.on_join,
            "UserLeave": self.on_leave
        }
        self._init_commands()
        self.bot_data = {"username": "Potato"}  # TODO: Fix
        self.channel_data = {"token": "Salad"}  # TODO: Fix
        self.config = {
            "points": {"name": "Bowls"},
            "auth": {"username": "Potato"}
        }  # TODO: Fix
        self.update_config = lambda *args: None  # TODO: Fix
        # self.send_message = lambda *args: print("SENDING", args)  # TODO Fix
        # self.get_channel = lambda *args: {{"user": {"social": {}}}}.update(
        #     self.channel_data)  # TODO: Fix
        # self._request = lambda *args: {}

    def _init_commands(self):
        """Initialize built-in commands."""

        self.commands = {  # TODO: dynamic-ify
            "cactus": "Ohai! I'm CactusBot. :cactus",
            "test": "Test confirmed. :cactus",
            "help": "Check out my documentation at cactusbot.readthedocs.org.",
            # "command": CommandCommand(),
            # "repeat": RepeatCommand(
            #     self.send_message,
            #     self.bot_data["username"],
            #     self.channel_data["token"]),
            # "quote": QuoteCommand(),
            # "social": SocialCommand(self.get_channel),
            # "uptime": UptimeCommand(self._request),
            # "friend": FriendCommand(self.get_channel),
            # "points": PointsCommand(self.config["points"]["name"]),
            # "spamprot": SpamProtCommand(self.update_config),
            # "pro": ProCommand(),
            # "sub": SubCommand(),
            # "cube": CubeCommand(),
            # "temmie": TemmieCommand()
        }

    async def handle(self, response):  # TODO: remove
        """Handle responses from a Beam websocket."""

        print("RESPONSE", response)

        data = response["data"]

        if "event" in response:
            if response["event"] in self.events:
                await self.events[response["event"]](data)
            else:
                self.logger.debug("No handler found for event {}.".format(
                    response["event"]
                ))
        elif isinstance(data, dict) and data.get("authenticated"):
            await self.send("CactusBot activated. Enjoy! :cactus")

    async def on_message(self, data):  # TODO: move parts to Beam, generalize
        """Handle chat message packets from Beam."""

        parsed = ''.join([
            chunk["data"] if chunk["type"] == "text" else chunk["text"]
            for chunk in data["message"]["message"]
        ])

        self.logger.info("{bot}{me}[{user}] {message}".format(
            bot='$ ' if data["user_name"] == self.config["auth"]["username"]
                else '',
            me='*' if data["message"]["meta"].get("me") else '',
            user=data["user_name"] + " > " + self.config["auth"]["username"]
                if data["message"]["meta"].get("whisper")
                else data["user_name"],
            message=parsed)
        )

        user = session.query(User).filter_by(id=data["user_id"]).first()
        if user is not None:
            user.messages += 1
            session.commit()
        else:
            user = User(id=data["user_id"], joins=1, messages=1)
            session.add(user)
            session.commit()

        # TODO: move spamprot o handler
        # mod_roles = ("Owner", "Staff", "Founder", "Global Mod", "Mod")
        # if not (data["user_roles"][0] in mod_roles or user.friend):
        #     if (len(parsed) > self.config["spam_protection"].get(
        #             "maximum_message_length", 256)):
        #         self.remove_message(data["channel"], data["id"])
        #         user.offenses += 1
        #         session.commit()
        #         return self.send_message(
        #             data["user_name"], "Please stop spamming.",
        #             method="whisper")
        #     elif (sum(char.isupper() for char in parsed) >
        #             self.config["spam_protection"].get(
        #                 "maximum_message_capitals", 32)):
        #         self.remove_message(data["channel"], data["id"])
        #         user.offenses += 1
        #         session.commit()
        #         return self.send_message(
        #             data["user_name"], "Please stop speaking in all caps.",
        #             method="whisper")
        #     elif (sum(chunk["type"] == "emoticon"
        #               for chunk in data["message"]["message"]) >
        #             self.config["spam_protection"].get(
        #             "maximum_message_emotes", 8)):
        #         self.remove_message(data["channel"], data["id"])
        #         user.offenses += 1
        #         session.commit()
        #         return self.send_message(
        #             data["user_name"], "Please stop spamming emoticons.",
        #             method="whisper")
        #     elif (findall(("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
        #                    "[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"),
        #                   parsed) and not
        #             self.config["spam_protection"].get(
        #                 "allow_links", False)):
        #         self.remove_message(data["channel"], data["id"])
        #         user.offenses += 1
        #         session.commit()
        #         return self.send_message(
        #             data["user_name"], "Please stop posting links.",
        #             method="whisper")

        # TODO: move to handler
        if parsed == "/cry":
            self.remove_message(data["channel"], data["id"])
            return self.send_message("/me cries with {} :'(".format(
                data["user_name"]))

        # TODO: move to handler
        if len(parsed) > 1 and parsed[0].startswith("!"):
            args = parsed.split()

            if args[0][1:] in self.commands:
                response = self.commands[args[0][1:]]
                if isinstance(response, str):
                    messages = response
                else:
                    messages = response(args, data)
            else:
                options = [
                    ('-'.join(args[:2])[1:], ['-'.join(args[:2])] + args[2:]),
                    (args[0][1:], args)
                ]

                for parse_method in options:
                    command = session.query(
                        Command).filter_by(command=parse_method[0]).first()
                    if command:
                        messages = command(
                            parse_method[1], data,
                            channel_name=self.channel_data["token"]
                        )
                        break
                else:
                    messages = "Command not found."

            if isinstance(messages, str):
                messages = (messages,)

            if data["message"]["meta"].get("whisper", False):
                for message in messages:
                    await self.send(
                        data["user_name"], message, method="whisper")
            else:
                await self.send(*messages)

    async def on_join(self, data):  # TODO: generalize
        """Handle user join packets from Beam."""
        # return "NO DELURKING PEOPLE! ._."  # TODO: fix

        user = session.query(User).filter_by(id=data["id"]).first()

        if not user:
            user = User(id=data["id"], joins=1)
        else:
            session.add(user)
            user.joins += 1
        session.commit()

        await self.send(
            super(BeamHandler, self).on_join(data["username"])
        )

    async def on_leave(self, data):  # TODO: generalize
        """Handle user leave packets from Beam."""
        # return "NO DELURKING PEOPLE! ._."  # TODO: fix

        await self.send(
            super(BeamHandler, self).on_leave(data["username"])
        )
