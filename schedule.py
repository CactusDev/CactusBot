from sqlalchemy.orm import Session
from sqlalchemy import event
from time import time
from asyncio import coroutine, get_event_loop, sleep, async
from collections import OrderedDict
from models import session, Schedule
from user import User
from uuid import uuid1


class Scheduler:

    session = Session()

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

    def add_to_db(self, obj):
        if obj.interval in self.scheduled:
            self.scheduled[obj.interval].insert(0, obj)
        else:
            self.scheduled[obj.interval] = [obj]

    @event.listens_for(Schedule, "after_insert")
    def on_add(mapper, connection, target, *args):
        print("on_add")
        print(args)
        self.add_to_db(target)

    def scheduled_add(self, text, interval, type="msg"):
        """Add a scheduled command to the DB
        Expecting:
            - Message's text
            - Message's type (Bot Command/Text Message)
            - Interval in full seconds (eg, no 1.5seconds)"""

        c = Schedule(text=text, interval=interval, type=type, uid=uuid1().urn)

        # Add the new scheduled sqlalchemy object to the list of cmds\
        if interval in self.scheduled:
            self.scheduled[interval].insert(0, c)
        else:
            self.scheduled[interval] = [c]

        session.add(c)
        session.flush()
        session.commit()

        return "Scheduled message [{id} - {msg}] will be run every {x} seconds!".format(id=c.id, msg=text, x=interval)

    def scheduled_remove(self, id):
        # Find the command that matches the ID
        query = session.query(Schedule).filter_by(id=id).first()

        # Did that query return any results for that ID?
        if query:
            interval = query.interval
            session.delete(query)
            print(query)
            if query in self.scheduled[interval]:
                self.scheduled[interval].remove(query)

            session.commit()
        # There was no result, so return an error message
        else:
            return "Scheduled message {id} doesn't exist!".format(id=text[0])

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
                    async(self.send_message(get_message(scheduled_msg)))
                else:
                    async(self.send_message(scheduled_msg.text))

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
