from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from os.path import abspath, dirname, join
from datetime import datetime
from re import sub, findall

basedir = abspath(dirname(__file__))
engine = create_engine('sqlite:///' + join(basedir, 'data/data.db'))
Base = declarative_base()

session = Session(engine)


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, unique=True, primary_key=True)

    command = Column(String, unique=True)
    response = Column(String)

    calls = Column(Integer, default=0)

    author = Column(Integer)
    creation = Column(DateTime)

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
            if args[1] in ("add", "remove"):
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
                        return "Added command !{}.".format(args[2])
                    else:
                        return "Not enough arguments!"
                elif args[1] == "remove":
                    if len(args) > 2:
                        q = session.query(Command).filter_by(command=args[2])
                        if q.first():
                            q.delete()
                            return "Removed command !{}.".format(args[2])
                        else:
                            return "!{} does not exist!".format(args[2])
                    else:
                        return "Not enough arguments!"
                session.commit()
        else:
            return "!command is moderator-only."


class CubeCommand(Command):
    def __call__(self, args, data=None):
        if args[1] == '2' and len(args) == 2:
            return "8! Whoa, that's 2Cubed!"
        elif len(findall("\d+", ' '.join(args[1:]))) > 8:
            return "Whoa! That's 2 many cubes!"
        nums = sub(
            "(\d+)",
            lambda match: str(int(match.groups()[0])**3),
            ' '.join(args[1:])
        )
        return nums


class Friend(Base):
        __tablename__ = "friends"

        id = Column(Integer, unique=True, primary_key=True)

        username = Column(String, unique=True)


class ChatFriends:
    session = session

    def add_friend(self, username):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            c = Friend(
                username=username
            )
            session.add(c)
        session.commit()

    def remove_friend(self, username):
        query = session.query(Base).filter_by(username=username).first()

        if query:
            query.delete()
            return True
        return False


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


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, unique=True, primary_key=True)
    author = Column(String, unique=True)
    quote = Column(String, unique=True)


class Quotes:

    def add_quote(self, quote, author):
        q = Quote(
            author=author,
            quote=quote
        )

        session.add(q)
        session.commit()

    def remove_quote(self, quote, author):
        query = session.query(Base).filter_by(id=id).first()

        if query:
            query.delete()
            return True
        return False
