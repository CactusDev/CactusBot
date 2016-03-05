from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from os.path import abspath, dirname, join
from datetime import datetime

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


class CommandFactory:
    session = session

    def add_command(self, command, response, author):
        query = session.query(Command).filter_by(command=command).first()
        if query:
            query.response = response
        else:
            c = Command(
                command=command,
                response=response,
                creation=datetime.utcnow(),
                author=author
            )
            session.add(c)
        session.commit()

    def remove_command(self, command):
        query = session.query(Base).filter_by(command=command).first()

        if query:
            query.delete()
            return True
        return False


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
