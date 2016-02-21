from requests import Session


def request(self, req, url, *args, **kwargs):
    """Send HTTP request to Beam."""
    self.session = Session()

    if req.lower() in ('get', 'head', 'post', 'put', 'delete', 'options'):
        response = self.session.__getattribute__(req.lower())(
            self.path + url, *args, **kwargs
        )

        if 'error' in response.json().keys():
            self.logger.warn("Error: {}".format(response.json()['error']))

        return response.json()
    else:
        self.logger.debug("Invalid request: {}".format(req))
