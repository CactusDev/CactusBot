from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

from functools import wraps, partial

from os.path import abspath, dirname, join
from datetime import datetime

from re import sub, findall
from random import randrange, choice

from tornado.ioloop import PeriodicCallback

basedir = abspath(dirname(__file__))
engine = create_engine("sqlite:///" + join(basedir, "data/data.db"))
Base = declarative_base()

session = Session(engine)


def role_specific(*roles, reply=None):
    roles += ("Owner",)

    def role_specific_decorator(function):
        @wraps(function)
        def wrapper(self, args, data):
            if any(filter(lambda r: r in data["user_roles"], roles)):
                return function(self, args, data)
            r = reply if reply else roles[0].lower() if roles else "permission"
            return "This command is {}-only!".format(r)
        return wrapper
    return role_specific_decorator

mod_only = role_specific("Founder", "Staff", "Global Mod", "Mod", reply="mod")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, unique=True, primary_key=True)

    command = Column(String, unique=True)
    response = Column(String)

    calls = Column(Integer, default=0)

    creation = Column(DateTime)
    author = Column(Integer)

    perms = Column(String)
    allowed = Column(String)

    repeat = relationship("Repeat", backref="command")

    def __call__(self, args, data, channel_name=None):
        response = self.response

        perms = [perm for perm in self.perms]
        user_roles = data["user_roles"]
        # If it's the channel owner, ignore all perm checking
        if "Owner" not in user_roles:
            for perm in perms:
                # Mod-only command
                if perm == "+":
                    if "Mod" not in user_roles:
                        # Mod-only, so don't return anything
                        return None

                # Owner-only command
                elif perm == "~":
                    if "Owner" not in user_roles:
                        # Owner-only, so don't return anything
                        return None

                # Sub-only command
                elif perm == "$":
                    if "Subscriber" not in user_roles and "Mod" not in user_roles:
                        # Subscriber-only, so don't return anything
                        return None

        response = response.replace("%name%", data["user_name"])

        try:
            response = sub(
                "%arg(\d+)%",
                lambda match: args[int(match.group(1))],
                response
            )
        except IndexError:
            return "Not enough arguments!"

        response = response.replace("%args%", ' '.join(args[1:]))

        self.calls += 1
        session.commit()

        response = response.replace("%count%", str(self.calls))

        response = response.replace(
            "%channel%",
            channel_name if channel_name else data["id"]
        )

        # Check for kapooyah commands
        if "-" in perms:
            pass

        return response


class Repeat(Base):
    __tablename__ = "repeating"

    id = Column(Integer, unique=True, primary_key=True)

    command_object = relationship("Command", backref="command_object")
    command_name = Column(String, ForeignKey("commands.command"))

    arguments = Column(String)

    interval = Column(Integer)


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, unique=True, primary_key=True)

    quote = Column(String)

    creation = Column(DateTime)
    author = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True)

    friend = Column(Boolean, default=False)

    joins = Column(Integer, default=0)
    messages = Column(Integer, default=0)
    offenses = Column(Integer, default=0)

    points = Column(Integer, default=0)


class CommandCommand(Command):

    @mod_only
    def __call__(self, args, data):
        if args[1] == "add":
            if len(args) > 3:
                keys = ("+", "-", "~", "$")
                perms = [perm for perm in list(args[2]) if perm in keys]
                cmd = [char for char in list(args[2]) if char not in keys]

                cmd = "".join(cmd)
                perms = "".join(perms)

                command = session.query(Command).filter_by(
                    command="".join(cmd)).first()

                if command:
                    command.response = ' '.join(args[3:])
                else:
                    command = Command(
                        command=cmd,
                        response=' '.join(args[3:]),
                        creation=datetime.utcnow(),
                        author=data["user_id"],
                        perms=perms
                    )

                    session.add(command)
                    session.commit()
                return "Added command !{}.".format("".join(cmd))
            return "Not enough arguments!"
        elif args[1] == "remove":
            if len(args) > 2:
                command = session.query(Command).filter_by(
                    command=args[2])
                if command.first():
                    command.delete()
                    session.commit()
                    return "Removed command !{}.".format(args[2])
                return "!{} does not exist!".format(args[2])
            return "Not enough arguments!"
        elif args[1] == "list":
            commands = session.query(Command).all()
            return "Commands: {commands}".format(
                commands=', '.join([c.command for c in commands if c.command]))
        return "Invalid argument: {}.".format(args[1])


class QuoteCommand(Command):

    @mod_only
    def __call__(self, args, data):
        if len(args) > 1:
            try:
                id = int(args[1])
                return session.query(Quote).filter_by(id=id).first().quote
            except ValueError:
                pass
            except AttributeError:
                return "Undefined quote with ID {}.".format(id)

            if len(args) > 2:
                if args[1] == "add":
                    quote = Quote(
                        quote=' '.join(args[2:]),
                        creation=datetime.utcnow(),
                        author=data["user_id"]
                    )
                    session.add(quote)
                    session.flush()
                    session.commit()
                    return "Added quote with ID {}.".format(quote.id)
                elif args[1] == "remove":
                    try:
                        id = int(args[2])
                    except ValueError:
                        return "Invalid quote ID '{}'.".format(args[2])
                    quote = session.query(Quote).filter_by(id=id)
                    if quote.first():
                        quote.delete()
                        session.commit()
                        return "Removed quote with ID {}.".format(args[2])
                    return "Quote {} does not exist!".format(args[2])
                return "Invalid argument: '{}'.".format(args[1])
            return "Not enough arguments."
        else:
            if not session.query(Quote).count():
                return "No quotes added."
            random_id = randrange(0, session.query(Quote).count())
            return session.query(Quote)[random_id].quote


class SocialCommand(Command):

    def __init__(self, get_channel):
        super(SocialCommand, self).__init__()
        self.get_channel = get_channel

    def __call__(self, args, data=None):
        s = self.get_channel(data["channel"])["user"]["social"]
        a = [arg.lower() for arg in args[1:]]
        if s:
            if not a:
                return ', '.join(': '.join((k.title(), s[k])) for k in s)
            elif set(a).issubset(set(s)):
                return ', '.join(': '.join((k.title(), s[k])) for k in a)
            return "Data not found for service{s}: {}.".format(
                ', '.join(set(a) - set(s)), s='s'*(len(set(a) - set(s)) != 1))
        return "No social services were found on the streamer's profile."


class CubeCommand(Command):

    def __call__(self, args, data=None, **kwargs):
        if args[1] == '2' and len(args) == 2:
            return "8! Whoa, that's 2Cubed!"

        numbers = findall(
            "( [0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)",
            ' ' + ' '.join(args[1:]) + ' '
        )

        if len(numbers) == 0:
            return "{w[0]}{response}{w[1]}³".format(
                response=' '.join(args[1:]),
                w='  ' if findall(":\w+$", ' '.join(args[1:])) else '()'
            )
        elif len(numbers) > 8:
            return "Whoa! That's 2 many cubes!"

        return sub(
            "( [0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)",
            lambda match: " {:g} ".format(float(match.groups()[0]) ** 3),
            ' ' + ' '.join(args[1:]) + ' '
        )


class UptimeCommand(Command):

    def __call__(self, args, data=None):
        return "In development. :cactus"


class PointsCommand(Command):

    def __init__(self, points_name):
        super(PointsCommand, self).__init__()
        self.points_name = points_name

    def __call__(self, args, data):
        if len(args) > 1:
            return "Points update in development. :cactus"
        user = session.query(User).filter_by(id=data["user_id"]).first()
        return "@{user} has {amount} {name}.".format(
            user=data["user_name"],
            amount=user.points,
            name=self.points_name + ('s' if user.points != 1 else ''))


class RepeatCommand(Command):

    def __init__(self, send_message, bot_name, channel):
        super(RepeatCommand, self).__init__()
        self.send_message = send_message
        self.data = {"user_name": bot_name}
        self.channel = channel

        self.repeats = dict()

        for repeat in session.query(Repeat).all():
            periodic_callback = PeriodicCallback(
                partial(self.send, repeat),
                repeat.interval * 1000
            )
            self.repeats[repeat.command.command] = periodic_callback
            periodic_callback.start()

    @mod_only
    def __call__(self, args, data):
        if args[1] == "add":
            if len(args) > 3:
                try:
                    interval = int(args[2])
                except ValueError:
                    return "Invalid interval: '{}'.".format(args[2])

                repeat = session.query(Repeat).filter_by(
                    command_name=args[3]).first()

                if repeat:
                    repeat.interval = interval
                    repeat.arguments = ' '.join(args[3:])
                    periodic_callback = self.repeats[repeat.command.command]
                    periodic_callback.callback_time = interval * 1000
                    periodic_callback.stop()
                    periodic_callback.start()
                    session.add(repeat)
                    session.commit()
                    return "Repeat updated."

                command = session.query(Command).filter_by(command=args[3])
                if command.first():
                    command = command.first()
                    repeat = Repeat(
                        command_object=command,
                        interval=interval,
                        arguments=' '.join(args[3:])
                    )

                    periodic_callback = PeriodicCallback(
                        partial(self.send, repeat),
                        interval * 1000
                    )
                    self.repeats[args[3]] = periodic_callback
                    periodic_callback.start()
                    session.add(repeat)
                    session.commit()
                    return "Repeating command '!{}' every {} seconds.".format(
                        command.command, interval)
                return "Undefined command '!{}'.".format(args[3])
            return "Not enough arguments!"
        elif args[1] == "remove":
            if len(args) > 2:
                repeat = session.query(Repeat).filter_by(command_name=args[2])
                if repeat.first():
                    self.repeats[args[2]].stop()
                    del self.repeats[args[2]]
                    repeat.delete()
                    session.commit()
                    return "Removed repeat for command !{}.".format(args[2])
                return "Repeat for !{} does not exist!".format(args[2])
            return "Not enough arguments!"
        elif args[1] == "list":
            repeats = session.query(Repeat).all()
            return "Repeats: {repeats}".format(
                repeats=', '.join(
                    [r.command.command+' '+str(r.interval) for r in repeats]
                )
            )
        return "Invalid argument: {}.".format(args[1])

    def send(self, repeat):
        self.send_message(
            repeat.command(
                repeat.arguments.split(),
                self.data,
                channel_name=self.channel
            )
        )


class TemmieCommand(Command):
    quotes = [
        "fhsdhjfdsfjsddshjfsd",
        "hOI!!!!!! i'm tEMMIE!!",
        "awwAwa cute!! (pets u)",
        "OMG!! humans TOO CUTE (dies)",
        "NO!!!!! muscles r... NOT CUTE",
        "NO!!! so hungr... (dies)",
        "FOOB!!!",
        "can't blame a BARK for tryin'..."
    ]

    def __call__(self, args=None, data=None):
        return choice(self.quotes)


class FriendCommand(Command):

    def __init__(self, get_channel):
        super(FriendCommand, self).__init__()
        self.get_channel = get_channel

    @mod_only
    def __call__(self, args, data):
        if len(args) == 2:
            id = self.get_channel(args[1])["user"]["id"]
            query = session.query(User).filter_by(id=id).first()
            if query:
                query.friend = not query.friend
                session.commit()
                return "{}ed @{} as a friend.".format(
                    ["Remov", "Add"][query.friend], args[1])
            else:
                return "User has not entered this channel."
        elif len(args) > 2:
            return "Too many arguments."
        else:
            return "Not enough arguments."

    def remove_points(self, username, amount):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            session.delete(query)
            return True
        return False


class SpamProtCommand(Command):

    def __init__(self, update_config):
        super(SpamProtCommand, self).__init__()
        self.update_config = update_config

    @mod_only
    def __call__(self, args, data=None):
        if len(args) >= 3:
            if args[1] == "length":
                if args[2].isdigit():
                    self.update_config(
                        "spam_protection.maximum_message_length",
                        int(args[2]))
                    return "Maximum message length set to {}.".format(
                        args[2])
                return "Invalid number: '{}'.".format(args[2])
            elif args[1] == "caps":
                if args[2].isdigit():
                    self.update_config(
                        "spam_protection.maximum_message_capitals",
                        int(args[2]))
                    return "Maximum capitals per message set to {}.".format(
                        args[2])
                return "Invalid number: '{}'.".format(args[2])
            elif args[1] == "emotes":
                if args[2].isdigit():
                    self.update_config(
                        "spam_protection.maximum_message_emotes",
                        int(args[2]))
                    return "Maximum emotes per message set to {}.".format(
                        args[2])
                return "Invalid number: '{}'.".format(args[2])
            elif args[1] == "links":
                if args[2].lower() in ("true", "false"):
                    links_allowed = args[2].lower() == "true"
                    self.update_config(
                        "spam_protection.allow_links",
                        links_allowed)
                    return "Links are now {dis}allowed.".format(
                        dis="dis" * (not links_allowed))
                return "Invalid true/false: '{}'.".format(args[2])
            return "Invalid argument: '{}'.".format(args[1])
        return "Not enough arguments."


class ProCommand(Command):

    @role_specific("Pro", reply="pro")
    def __call__(self, args=None, data=None):
        return "I'm such a Pro! B)"


class SubCommand(Command):

    @role_specific("Subscriber", reply="sub")
    def __call__(self, args=None, data=None):
        return "I'm a subscriber! :salute"
