
from asyncio import coroutine


class Server:

    pid = 0
    packet = ""

    @coroutine
    def connect(self, username):
        print("Connecting to the live-socket")
        # print("Connected to the live-socket")
