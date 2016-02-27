from exceptions import BadSessionException
import json


def request(parent, req, url, packet, **kwargs):
    """Send HTTP request to Beam."""

    if req.lower() in ('get', 'head', 'post', 'put', 'delete', 'options'):
        response = parent.session.__getattribute__(req.lower())(
            parent.path + url, data=packet
        )

        if 'error' in response.json().keys():
            parent.logger.warn("Error: {}".format(response.json()['error']))

        return response.json()
    else:
        parent.logger.debug("Invalid request: {}".format(req))
        raise BadSessionException(req.lower)


def get_server(self, id):
    req = request(self, "GET", "/chats/{id}".format(id=id), packet={})
    req = json.load(req)

    return req['endpoints'][0]


def get_authkey(self, id):
    req = request(self, "GET", "/chats/{id}".format(id=id), packet={})
    req = json.load(req)

    return req['authkey']


def get_id(self, username):
    req = request(self, "GET", "/channels/{user}".format(user=username), packet={})
    req = json.loads(req)

    return req['id']
