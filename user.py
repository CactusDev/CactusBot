from requests import Session


class User:
    path = path = "https://beam.pro/api/v1"

    def getChannelID(self, username):
        userJSON = self.session.get(self.path + "/channels/{user}".format(
            user=username)).json()

        return self.session.get(userJSON.get('id'))

    def __init__(self):
        self.session = Session()

    def get(self, url, **kwargs):
        return self.session.get(self.path + url, **kwargs)

    def head(self, url, **kwargs):
        return self.session.head(self.path + url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.session.post(self.path + url, data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(self.path + url, data, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(self.path + url, **kwargs)

    def options(self, url, **kwargs):
        return self.session.options(self.path + url, **kwargs)

    def login(self, username, password, code):
        """Authenticate and login with Beam."""
        auth = {
            "username": username,
            "password": password,
            "code": code
        }

        channel_data = self.post("/users/login", auth).json()

        if 'error' in channel_data.keys():
            raise Exception(channel_data.get('message', ''))

        return channel_data
