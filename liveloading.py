
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

    def check_partnered(self, username):
        user = User()
        req = user.get_channel(username, fields='partnered')
        partnered = req['partnered']

        return partnered

    @coroutine
    def live_connect(self, username):
        print("Connecting to the live-socket")

        ws = create_connection('wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket')
        self.packet_recv = ws.recv()
        status = str(self.packet_recv.split()[0][0])

        is_partnered = self.check_partnered(username)
        user_id = str(self.get_channel(username, fields='id')['id'])

        if status == "0":
            # Subscribing to channel events
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + user_id + ':update"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            self.pid += 1

            # Subscribing to user events
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["user:' + user_id + ':update"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            self.pid += 1

            # Subscribe to follows
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + user_id + ':followed"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            self.pid += 1

            # Subscribe to subs if needed

            if is_partnered:
                self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + user_id + ':subscribed"]},"url":"/api/v1/live"}]'
                ws.send(self.packet_send)

                self.pid += 1

                self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:' + user_id + ':resubscribed"]},"url":"/api/v1/live"}]'
                ws.send(self.packet_send)

                self.pid += 1

            self.packet_recv = ws.recv()
            status = str(self.packet_recv.split()[0][:2])
        else:
            raise Exception("Something terrible happened!")

        if status == "40":
            ws.send("2")
            self.packet_recv = ws.recv()
            status = str(self.packet_recv.split()[0][:2])
        else:
            raise Exception("Something bad went wrong")

        if status == "42":
            print("Connected to the live-socket")

            try:
                while True:
                    recv = str(ws.recv())
                    print(recv)

                    if "viewersCurrent" in recv:
                        self.total_index += 1
                        recv = recv[2:]
                        data = loads(recv)
                        curr = data[1]['viewersCurrent']
                        self.total_viewer += curr
                    elif "viewersTotal" in recv:
                        recv = recv[2:]
                        data = loads(recv)
                        curr = data[1]['viewersTotal']

                        self.total_viewed = curr
                    elif "followed" in recv:
                        recv = recv[2:]
                        data = loads(recv)
                        is_following = (data[1]['following'])

                        if is_following is True:
                            self.total_followers += 1
                            print(data)
                            yield from self.send_message("Thanks for the follow, {user}".format(user=""))
                        else:
                            self.total_unfollowers += 1
                    elif "subscribed" in recv:
                        self.total_subs += 1
                    elif "resubscribed" in recv:
                        self.total_resubs += 1

            except:
                if self.total_index is 0:
                    print("Not enough samples.")

                average = self.total_viewer / self.total_index

                with open('data/stats.json', 'r+') as f:
                    stats = load(f)

                    stats['average-viewers'] = average
                    stats['total-views'] = curr

                    curr_followers = stats['total-followers']
                    stats['total-followers'] = (self.total_followers + int(curr_followers))

                    curr_unfollows = stats['total-unfollows']
                    stats['total-unfolows'] = (self.total_unfollows + int(curr_unfollows))

                    dump(stats, f, indent=4, sort_keys=True)

                exit()
