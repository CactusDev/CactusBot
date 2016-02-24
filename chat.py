from utils import request
import json
import websocket


def get_id_from_name(username):
    raw = json.loads(request("GET", "/channels/{username}?fields=id"))
    return raw['id']


def connect(server, authkey):
    ws = websocket.WebSocketApp(server)
    ws.send('''{"type":"method","method":"auth","arguments":[{id},{channeID},"{auth}"],"id":{id}}''')
    result = ws.recv()
    print(result)
    ws.run_forever(sslopt={"check_hostname": False})


def get_server(username):
    raw = request("GET", "/chats/{id}".format(id=get_id_from_name(username)))
    data = json.loads(raw)

    address = data["endpoints"][0]
