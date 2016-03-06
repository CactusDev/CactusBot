from sqlalchemy.orm import Session

from time import time

from asyncio import coroutine, get_event_loop, sleep

from collections import OrderedDict

from functools import partial


class Scheduler:

    def init_scheduler(self):
        self.scheduled = {}
        scheduled_db = [{"interval": 3, "message": "foo", "type": "msg"}, {"interval": 3, "message": "bar", "type": "msg"}, {"interval": 2, "message": "!bar", "type": "cmd"}, {"interval": 17, "message": "bah", "type": "msg"}]
        # scheduled_db = sqlalchemy return list of all scheduled commands
        # Populate list of all scheduled commands at their proper times
        for msg in scheduled_db:
            # Check if the interval already exists in self.scheduled
            if msg["interval"] in self.scheduled:
                self.scheduled[msg["interval"]].append(msg)
            else:
                self.scheduled[msg["interval"]] = [msg]

        self.scheduled = OrderedDict(sorted(self.scheduled.items()))

        self.init_time = int(time())

        interval = list(self.scheduled.items())[0][0]

        self.loop.call_later(interval, self.scheduled_handler)

        # print(self.scheduled)

    def add(self, text, type, interval):
        """Add a scheduled command to the DB
        Expecting:
            - Message's text
            - Message's type (Bot Command/Text Message)
            - Interval in full seconds (eg, no 1.5seconds)"""
        session = Session()

        query = session.query(Scheduled.Base).first()

        if query:
            c = Scheduled(
                text=text,
                interval=interval,
                type=type,
                last_ran=int(time)
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

    def scheduled_handler(self):
        """This function is the scheduler call_later callback function
        It handles sending the scheduled message & setting the next callback"""
        print(list(self.scheduled.items())[0])
        pass
