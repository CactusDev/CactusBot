from sqlalchemy.orm import Session
from time import time
from asyncio import coroutine, get_event_loop, sleep
from collections import OrderedDict
from models import session, Schedule


class Scheduler:

    def init_scheduler(self):
        self.scheduled = {}
        self.active_msgs = []
        self.run_msgs = []
        scheduled_db = [
            {"interval": 3, "message": "foo", "type": "msg", "uid": "bdc5aedce56f11e5b019448a5b8774ea"},
            {"interval": 3, "message": "bar", "type": "msg", "uid": "c5c3a012e56f11e5b019448a5b8774ea"},
            {"interval": 2, "message": "bar", "type": "cmd", "uid": "bb9f1fa8e56f11e5b019448a5b8774ea"},
            {"interval": 5, "message": "bah", "type": "msg", "uid": "caa1fa7ae56f11e5b019448a5b8774ea"}
        ]

        scheduled_db = session.query(Schedule)

        print(scheduled_db)

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

        for msg in self.scheduled.items():
            callback_time = int(time() + msg[0])
            self.loop.call_later(msg[0], self.scheduled_handler, msg[0], callback_time, msg[1])
            self.active_msgs.append(callback_time)
            self.run_msgs.append(msg[1][0]["uid"])

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

    def scheduled_handler(self, interval, prev_call, group):
        """This function is the scheduler call_later callback function
        It handles sending the scheduled message & setting the next callback"""
        # print("Callback")
        # print("interval:\t", interval)
        # print("prev_call:\t", prev_call)
        next_call = int(time() + interval)
        # print("next_call:\t", next_call)

        while True:
            # Is there already another callback scheduled for that future time?
            if next_call in self.active_msgs:
                # Yes, so go to next iteration of the loop
                next_call += interval
                continue
            else:
                """
                Pop top message into prev_msg from group
                Append prev_msg to group"""

                self.active_msgs.remove(prev_call)
                self.active_msgs.append(next_call)
                self.loop.call_later(interval, self.scheduled_handler, interval, next_call, )
                break
