
from models import Scheduled
from sqlalchemy.orm import Session

from time import datetime

from asyncio import coroutine, get_event_loop


class Schedule:

    loop = get_event_loop()

    def add(self, text, interval):
        session = Session()

        query = session.query(Scheduled.Base).first()

        if query:
            c = Scheduled(
                text=text,
                interval=interval,
                last_ran=datetime.utcnow()
            )

            session.add(c)
            session.flush()
            session.commit()
        else:
            raise Exception("WHAT ARE YOU DOING?!")

    def remove(self, id):
        session = Session()
        query = session.query(Scheduled.Base).filter_by(id=id).first()

        if query:
            query.delete()
            session.commit()
        else:
            raise Exception("That shouldn't have happened.")

    @coroutine
    def schedule(self, id, interval):
        session = Session()
        cur_time = 0

        query = session.query(Scheduled.Base).filter_by(id=id).first()

        if query:
            pass
        else:
            raise Exception("Someting bad happened.")
