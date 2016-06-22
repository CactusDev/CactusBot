import tornado.web
import tornado.websocket
import tornado.ioloop
from sys import argv
from json import dumps
from json import loads
from datetime import timedelta


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("New client connected")
        # self.write_message("You are connected")

    def on_message(self, message):
        q = loads(message)
        if q["method"] == "auth":
            message = dumps({
                'data': {
                    'roles': ['Mod', 'User'],
                    'authenticated': True
                },
                'id': q["id"],
                'type': 'reply',
                'error': None
            })
        else:
            message = dumps({
                'event': 'ChatMessage',
                'type': 'event',
                'data': {
                    'id': '580dccc0-02be-11e6-a03b-dffa207c0c0d',
                    'user_name': 'Eight',
                    'channel': 2151,
                    'user_roles': ['Mod', 'User'],
                    'user_id': 44486,
                    'message': {
                        'message': [
                            {
                                'data': 'CactusBot! ',
                                'type': 'text'
                            }, {
                                'source': 'builtin',
                                'text': ':cactus',
                                'type': 'emoticon',
                                'coords': {'y': 22, 'x': 0},
                                'pack': 'memes'
                            }
                        ],
                        'meta': {}
                    }
                }
            })
        try:
            self.write_message(message)
            print("SENT", message)
        except Exception:
            pass
        finally:
            tornado.ioloop.IOLoop.instance().add_timeout(
                timedelta(seconds=5),
                self.close
            )

    def on_close(self):
        pass
        # print("Client disconnected")


application = tornado.web.Application([
    (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    application.listen(int(argv[1]))
    tornado.ioloop.IOLoop.instance().start()

# from tornado import web, websocket, ioloop
# class EchoServer(websocket.WebSocketHandler):
#     def on_message(self, message): print(message); self.write_message(message)
# web.Application([(r"/", EchoServer)]).listen(8888)
# ioloop.IOLoop.instance().start()
