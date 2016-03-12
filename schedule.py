from sqlalchemy.orm import Session
from time import time
from asyncio import coroutine, get_event_loop, sleep
from collections import OrderedDict
from models import session, Schedule
from User import User
from uuid import uuid1


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
        self.init_time = int(time())

        for msg in self.scheduled.items():
            callback_time = int(time() + msg[0])
            self.loop.call_later(msg[0],
                                 self.scheduled_handler,
                                 msg[0],
                                 callback_time,
                                 msg[1][0].uid)
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
                last_ran=int(time),
                uid=uuid1()
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

    def scheduled_handler(self, interval, prev_call, uid):
        """This function is the scheduler call_later callback function
        It handles sending the scheduled message & setting the next callback"""
        # print("Callback")
        next_call = int(time() + interval)

        while True:
            # Is there already another callback scheduled for that future time?
            if range(next_call - 3, next_call + 3) in self.active_msgs:
                # Yes, so add the interval to the call time again
                next_call += interval
                # Go to next iteration of the loop
                continue
            else:
                scheduled_msg = session.query(Schedule).filter_by(uid=uid).one()
                text = scheduled_msg.text

                # Is it the output of a bot command?
                if scheduled_msg.type == "cmd":
                    yield from self.send_message(get_message(scheduled_msg))
                else:
                    print(scheduled_msg.text)
                    yield from self.send_message(scheduled_msg.text)

                self.scheduled[interval].append(self.scheduled[interval].pop(0))

                # Remove the previous callback timestamp
                self.active_msgs.remove(prev_call)
                # Add the next callback timestamp so we can compare @ callback
                self.active_msgs.append(next_call)

                # Schedule next call
                self.loop.call_later(interval,
                                     self.scheduled_handler,
                                     interval,
                                     next_call,
                                     self.scheduled[interval][0].uid)
                break
