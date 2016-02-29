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

    calls = Column(Integer)

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
