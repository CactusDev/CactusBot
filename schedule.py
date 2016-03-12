from sqlalchemy.orm import Session
from time import time
from asyncio import coroutine, get_event_loop, sleep
from collections import OrderedDict
from models import session, Schedule
from User import User


class Scheduler:

    def init_scheduler(self):
        self.scheduled = {}
        self.active_msgs = []
        self.run_msgs = []

        scheduled_db = session.query(Schedule).all()

        # Populate list of all scheduled commands at their proper times
        for msg in scheduled_db:
            # Check if the interval already exists in self.scheduled
            if msg.interval in self.scheduled:
                self.scheduled[msg.interval].append(msg)
            else:
                self.scheduled[msg.interval] = [msg]

        self.scheduled = OrderedDict(sorted(self.scheduled.items()))

        print(self.scheduled)

        self.init_time = int(time())

        for msg in self.scheduled.items():
            callback_time = int(time() + msg[0])
            self.loop.call_later(msg[0], self.scheduled_handler, msg[0], callback_time)
            self.active_msgs.append(callback_time)

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

            # Add the new scheduled sqlalchemy object to the list of cmds
            self.scheduled[interval].insert(c, 0)

            session.add(c)
            session.flush()
            session.commit()
        else:
            raise Exception("There was an error in the adding.")

    def remove(self, id):
        session = Session()
        query = session.query(Scheduled.Base).filter_by(id=id).first()

        if query:
            query.delete()
            session.commit()
        else:
            raise Exception("There was an error in the removal.")

    def get_message(self, id):
        session = Session()

        query = session.query(Scheduled.Base).filter_by(id=id).first()

        if query:
            return query.text
        else:
            raise Exception("That doesn't exist.")

    def scheduled_handler(self, interval, prev_call):
        """This function is the scheduler call_later callback function
        It handles sending the scheduled message & setting the next callback"""
        print("Callback")
        print("interval:\t", interval, prev_call)
        next_call = int(time() + interval)

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

                yield from User().send_message(get_message(cur_msg))

                # Remove the first item in the list for the interval
                cur_msg = self.scheduled[interval].popitem(last=False)
                # Add it again, at the end of the list
                self.scheduled[interval].append(cur_msg)

                self.active_msgs.remove(prev_call)
                self.active_msgs.append(next_call)
                self.loop.call_later(interval, self.scheduled_handler, interval, next_call)
                break
