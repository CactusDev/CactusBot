from requests import Session


class User:
    path = path = "https://beam.pro/api/v1"

    def __init__(self):
        self.session = Session()

    def request(self, req, url, *args, **kwargs):
        if req.lower() in ('get', 'head', 'post', 'put', 'delete', 'options'):
            return self.session.__getattribute__(req.lower())(
                self.path + url, *args, **kwargs
            )

    def login(self, username, password, code=''):
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
