from websocket import create_connection
from socketIO_client import SocketIO, LoggingNamespace


class Server:

    pid = 0
    packet = ""

    def connect(self, username):
        print("Connecting to the live-socket")

        with SocketIO('realtime.beam.pro', 8000, LoggingNamespace) as socket:
            socket.emit(''' 'put',{"method":"put","headers":{},"data":{"slug":["channel:innectic:update"]},"url":"/api/v1/live"} ''')
            socket.wait(seconds=1)

        print("Connected to the live-socket")

server = Server()
server.connect('3326')
