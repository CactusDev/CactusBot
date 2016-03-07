
from websocket import create_connection
from user import User
import logging
from time import sleep
from json import loads, load, dump
from asyncio import coroutine


class Liveloading(User):

    pid = 0
    packet_recv = ""
    packet_send = ""
    status = 0

    total_viewer = 0
    total_index = 0
    total_viewed = 0

    total_followers = 0
    total_unfollows = 0

    total_subs = 0
    total_resubs = 0

    message_id = 100

    def check_partnered(self, username):
        user = User()
        req = user.get_channel(username, fields='partnered')
        partnered = req['partnered']

        return partnered

    @coroutine
    def live_connect(self, username):
        print("Connecting to the live-socket")

        is_partnered = self.check_partnered(username)
        user_id = self.get_channel(username)['id']
        print(user_id)

        ws = create_connection('wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket')
        packet_recv = ws.recv()
        status = str(packet_recv.split()[0][0])

        if status == "0":
            # Subscribing to channel events
            packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + str(user_id) + ':update"]},"url":"/api/v1/live"}]'
            ws.send(packet_send)
            self.pid += 1

            # Subscribing to user events
            packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["user:' + str(user_id) + ':update"]},"url":"/api/v1/live"}]'
            ws.send(packet_send)
            self.pid += 1

            # Subscribe to follows
            packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + str(user_id) + ':followed"]},"url":"/api/v1/live"}]'
            ws.send(packet_send)
            self.pid += 1

            # Subscribe to subs if needed

            if is_partnered:
                packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + str(user_id) + ':followed"]},"url":"/api/v1/live"}]'
                ws.send(packet_send)
                self.pid += 1

                packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + str(user_id) + ':followed"]},"url":"/api/v1/live"}]'
                ws.send(packet_send)
                self.pid += 1

            packet_recv = ws.recv()
            status = str(packet_recv.split()[0][:2])
        else:
            raise Exception("Something terrible happened!")

        if status == "40":
            ws.send("2")
            packet_recv = ws.recv()
            status = str(packet_recv.split()[0][:2])
        else:
            raise Exception("Something bad went wrong")

        if status == "42":
            print("Connected to the live-socket")

            while True:
                recv = str(ws.recv())

                if "viewersCurrent" in recv:
                    recv = recv[2:]
                    data = loads(recv)
                elif "viewersTotal" in recv:
                    recv = recv[2:]
                    data = loads(recv)
                elif "followed" in recv:
                    recv = recv[2:]
                    data = loads(recv)
                    is_following = (data[1]['following'])

                    if is_following is True:
                        yield from self.send_message("Thanks for the follow, {user}".format(user=""))
                    else:
                        print("UNFOLLOW")
