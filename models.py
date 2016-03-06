from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from os.path import abspath, dirname, join
from datetime import datetime
from re import sub, findall
from random import randrange

from user import User

basedir = abspath(dirname(__file__))
engine = create_engine('sqlite:///' + join(basedir, 'data/data.db'))
Base = declarative_base()

session = Session(engine)


class StoredCommand(Base):
    __tablename__ = "commands"

    id = Column(Integer, unique=True, primary_key=True)

    command = Column(String, unique=True)
    response = Column(String)

    calls = Column(Integer, default=0)

    creation = Column(DateTime)
    author = Column(Integer)


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, unique=True, primary_key=True)

    quote = Column(String)

    creation = Column(DateTime)
    author = Column(Integer)


class Command(StoredCommand, User):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def __call__(self, user, *args):
        response = self.response

        response = response.replace("%name%", user)

        try:
            response = sub(
                "%arg(\d+)%",
                lambda match: args[int(match.groups()[0])],
                response
            )
        except IndexError:
            return "Not enough arguments!"

        response = response.replace("%args%", ' '.join(args[1:]))

        self.calls += 1
        session.commit()

        response = response.replace("%count%", str(self.calls))

        return response


class CommandCommand(Command):
    def __call__(self, args, data):
        mod_roles = ("Owner", "Staff", "Founder", "Global Mod", "Mod")
        if data["user_roles"][0] in mod_roles:
            if args[1] == "add":
                if len(args) > 3:
                    q = session.query(Command).filter_by(command=args[2])
                    if q.first():
                        q.first().response = ' '.join(args[3:])
                    else:
                        c = Command(
                            command=args[2],
                            response=' '.join(args[3:]),
                            creation=datetime.utcnow(),
                            author=data["user_id"]
                        )
                        session.add(c)
                        session.commit()
                    return "Added command !{}.".format(args[2])
                else:
                    return "Not enough arguments!"
            elif args[1] == "remove":
                if len(args) > 2:
                    q = session.query(Command).filter_by(command=args[2])
                    if q.first():
                        q.delete()
                        session.commit()
                        return "Removed command !{}.".format(args[2])
                    else:
                        return "!{} does not exist!".format(args[2])
                else:
                    return "Not enough arguments!"
            else:
                return "Invalid argument: {}.".format(args[1])
        else:
            return "!command is moderator-only."


class QuoteCommand(Command):
    def __call__(self, args, data):
        mod_roles = ("Owner", "Staff", "Founder", "Global Mod", "Mod")
        if data["user_roles"][0] in mod_roles:
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
                        q = Quote(
                            quote=' '.join(args[2:]),
                            creation=datetime.utcnow(),
                            author=data["user_id"]
                        )
                        session.add(q)
                        session.flush()
                        session.commit()
                        return "Added quote with ID {}.".format(q.id)
                    elif args[1] == "remove":
                        try:
                            id = int(args[2])
                        except ValueError:
                            return "Invalid quote ID '{}'.".format(args[2])
                        q = session.query(Quote).filter_by(id=id)
                        if q.first():
                            q.delete()
                            session.commit()
                            return "Removed quote with ID {}.".format(args[2])
                        else:
                            return "Quote {} does not exist!".format(args[2])
                    else:
                        return "Invalid argument: '{}'".format(args[1])
                else:
                    return "Not enough arguments."
            else:
                random_id = randrange(0, session.query(Quote).count())
                return session.query(Quote)[random_id].quote
        else:
            return "!quote is moderator-only."


class SocialCommand(Command):
    user = User()

    def __call__(self, args, data=None):
        s = self.user.get_channel(data["channel"])["user"]["social"]
        a = [arg.lower() for arg in args[1:]]
        if s:
            if not a:
                return ', '.join(': '.join((k.title(), s[k])) for k in s)
            elif set(a).issubset(set(s)):
                return ', '.join(': '.join((k.title(), s[k])) for k in a)
            return "Data not found for service{s}: {}.".format(
                ', '.join(set(a)-set(s)), s='s'*(len(set(a)-set(s)) != 1))
        return "No social services were found on the streamer's profile."


class CubeCommand(Command):
    def __call__(self, args, data=None):
        if args[1] == '2' and len(args) == 2:
            return "8! Whoa, that's 2Cubed!"

        numbers = findall("\d+", ' '.join(args[1:]))

        if len(numbers) == 0:
            return "({})³".format(' '.join(args[1:]))
        elif len(numbers) > 8:
            return "Whoa! That's 2 many cubes!"

        nums = sub(
            "(\d+)",
            lambda match: str(int(match.groups()[0]) ** 3),
            ' '.join(args[1:])
        )
        return nums


class ScheduleCommand(Command):
    def __call__(self, args, data=None):
        action = args[1]
        interval = args[2]
        text = args[3]

        if action is "add":
            time = interval[:-1]
            modifer = interval[-1:]
        elif action is "remove":
            pass
        else:
            pass


class WhoAmICommand(Command):
    def __call__(self, args, data=None):
        return 'Ohai, {name}! Want a :cactus ?'.format(name=data['token'])


class UptimeCommand(Command):
    def __call__(self, args, data=None):
        return 'This isn\'t done yet. #BlameLiveLoading :cactus'


class CactusCommand(Command):
    def __call__(command):
        return 'Ohai! I\'m CactusBot! And you are?'

# #### TO BE REDONE IN USERS MODEL #### #


class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, unique=True, primary_key=True)
    user = Column(String, unique=True)
    amount = Column(Integer)


class UserPoints:
    session = Session

    def add_points(self, username, amount):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            c = Points(
                username=username,
                amount=amount
            )
            session.add(c)
            session.commit()
        else:
            # Todo add the user.
            pass
        session.commit()

    def remove_points(self, username, amount):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            query.delete()
            return True
        return False

    def set_points(self, username, amount):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            c = Points(
                username=username,
                amount=amount
            )
            session.add(c)
        else:
            # Todo add the user.
            pass
        session.commit()

    def reset_points(self, username):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            c = Points(
                username=username,
                amount=0
            )
            session.add(c)
        else:
            # TODO: Throw an error and tell the user that sent this bad things
            pass
        session.commit()


class Schedule(Base):
    __tablename__ = "scheduled"

    id = Column(Integer, unique=True, primary_key=True)
    text = Column(String)
    interval = Column(Integer)
    last_ran = Column(DateTime)
