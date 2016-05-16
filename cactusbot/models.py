from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

from functools import wraps

from os.path import abspath, dirname, join

from re import sub

# TODO: make dynamic
basedir = abspath(dirname(__file__))
engine = create_engine("sqlite:///" + join(basedir, "../data/data.db"))
Base = declarative_base()

session = Session(engine)


def role_specific(*roles, reply=None):
    roles += ("Owner",)

    def role_specific_decorator(function):
        @wraps(function)
        def wrapper(self, args, data, **kwargs):
            if any(filter(lambda role: role in data["user_roles"], roles)):
                return function(self, args, data, **kwargs)
            representation = (
                reply if reply
                else roles[0].lower().replace(' ', '-') if roles
                else "permission"
            )
            return "This command is {}-only!".format(representation)
        return wrapper
    return role_specific_decorator

all_roles = (
    "Founder", "Staff", "Global Mod", "Mod", "Subscriber", "Pro", "User"
)

mod_roles = ("Founder", "Staff", "Global Mod", "Mod")
mod_only = role_specific(*mod_roles, reply="mod")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, unique=True, primary_key=True)

    command = Column(String, unique=True)
    response = Column(String)

    calls = Column(Integer, default=0)

    creation = Column(DateTime)
    author = Column(Integer)

    permissions = Column(String)

    repeat = relationship("Repeat", backref="command")

    def __call__(self, args, data, **kwargs):
        if self.permissions:
            roles = str(self.permissions).split(',') + list(mod_roles)
        else:
            roles = all_roles

        @role_specific(*roles)
        def run_command(self, args, data, channel_name=None):
            response = self.response

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

            return response.split('\\n', 2)

        return run_command(self, args, data, **kwargs)


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
