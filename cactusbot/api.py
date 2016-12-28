"""Interact with CactusAPI."""

import json

from .services.api import API


class CactusAPI(API):
    """Interact with CactusAPI."""

    URL = "https://cactus.exoz.one/api/v1/"

    def __init__(self, token, auth_token="", **kwargs):
        super().__init__(**kwargs)

        self.token = token
        self.auth_token = auth_token

    async def request(self, method, endpoints, is_json=True, **kwargs):
        """Send HTTP request to endpoint."""

        headers = {
            "X-Auth-Token": self.token,
            "X-Auth-JWT": self.auth_token
        }

        if is_json:
            headers["Content-Type"] = "application/json"

        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        return await super().request(method, endpoints, **kwargs)

    async def login(self, password, *scopes):
        """Authenticate."""

        data = {
            "token": self.token,
            "password": password,
            "scopes": scopes
        }

        response = await self.post("/login", data=json.dumps(data))

        self.auth_token = (await response.json())["token"]

        return response

    async def get_command(self, name=None):
        """Get a command."""

        if name is not None:
            return await self.get(
                "/user/{token}/command/{command}".format(
                    token=self.token, command=name))
        return await self.get("/user/{token}/command".format(
            token=self.token))

    async def add_command(self, name, response, *, user_level=0):
        """Add a command."""

        data = {
            "response": response,
            "userLevel": user_level  # TODO
        }

        return await self.patch(
            "/user/{token}/command/{command}".format(
                token=self.token, command=name),
            data=json.dumps(data)
        )

    async def remove_command(self, name):
        """Remove a command."""

        return await self.delete("/user/{token}/command/{command}".format(
            token=self.token, command=name))

    async def get_command_alias(self, command):
        """Get a command alias."""
        return await self.get("/user/{token}/alias/{command}".format(
            token=self.token, command=command))

    async def add_alias(self, command, alias, args):
        """Create a command alias."""

        data = {
            "command": command,
            "arguments": args["message"]
        }

        return await self.patch("/user/{user}/alias/{alias}".format(
            user=self.token, alias=alias), data=json.dumps(data))

    async def remove_alias(self, alias):
        """Remove a command alias."""

        return await self.delete("/user/{user}/alias/{alias}".format(
            user=self.token, alias=alias))

    async def toggle_command(self, command, status):
        """Toggle the availability of a command."""

        data = {"enabled": status}

        return await self.patch("/user/{token}/command/{command}".format(
            token=self.token, command=command), data=json.dumps(data))

    async def update_command_count(self, command, action):
        """Set the count of a command."""

        data = {"count": action}

        return await(
            self.patch("/user/{token}/command/{command}/count".format(
                token=self.token, command=command), data=json.dumps(data)))

    async def get_quote(self, quote_id=None):
        """Get a quote."""

        if quote_id is not None:
            return await self.get("/user/{token}/quote/{id}".format(
                token=self.token, id=quote_id))
        return await self.get("/user/{token}/quote".format(
            token=self.token), params={"random": True})

    async def add_quote(self, quote):
        """Add a quote."""

        data = {"quote": quote}

        return await self.post(
            "/user/{token}/quote".format(token=self.token),
            data=json.dumps(data)
        )

    async def edit_quote(self, quote_id, quote):
        """Edit a quote."""

        data = {"quote": quote}

        return await self.patch(
            "/user/{token}/quote/{quote_id}".format(
                token=self.token, quote_id=quote_id),
            data=json.dumps(data)
        )

    async def remove_quote(self, quote_id):
        """Remove a quote."""

        return await self.delete("/user/{token}/quote/{id}".format(
            token=self.token, id=quote_id))

    async def get_friend(self, name=None):
        """Get a list of friends."""

        if name is None:
            return await self.get("/token/{token}/friend")

        return await self.get("/token/{token}/friend/{name}".format(
            token=self.token, name=name))

    async def add_friend(self, username):
        """Add a friend."""

        return await self.patch("/token/{token}/friend/{name}".format(
            token=self.token, name=username))

    async def remove_friend(self, username):
        """Remove a friend."""

        return await self.delete("/token/{token}/friend/{name}".format(
            token=self.token, name=username))

    async def get_config(self, *keys):
        """Get the token config."""

        if keys:
            return await self.get("/user/{token}/config".format(
                token=self.token), data=json.dumps({"keys": keys}))

        return await self.get("/user/{token}/config".format(
            token=self.token), is_json=False)

    async def update_config(self, value):
        """Update config attributes."""

        return await self.patch("/user/{user}/config".format(
            user=self.token), data=json.dumps(value))

    async def add_repeat(self, command, period, args):
        """Add a repeat."""

        data = {
            "commandName": command,
            "period": period,
            "arguments": args
        }

        return await self.post("/user/{user}/repeat".format(user=self.token),
                               data=json.dumps(data))

    async def remove_repeat(self, repeat):
        """Remove a repeat."""

        return await self.delete("/user/{user}/repeat/{repeat}".format(
            user=self.token, repeat=repeat))

    async def get_repeats(self):
        """Get all repeats."""

        return await self.get("/user/{user}/repeat".format(user=self.token))

    async def add_social(self, service, url):
        """Add a social service."""

        data = {"url": url}

        return await self.patch("/user/{user}/social/{service}".format(
            user=self.token, service=service), data=json.dumps(data))

    async def remove_social(self, service):
        """Remove a social service."""

        return await self.delete("/user/{user}/social/{service}".format(
            user=self.token, service=service))

    async def get_social(self, service=None):
        """Get social service."""

        if service is None:
            return await self.get("/user/{user}/social".format(
                user=self.token))
        return await self.get("/user/{user}/social/{service}".format(
            user=self.token, service=service))

    async def get_trusts(self, user_id=None):
        """Get all trusted users."""
        if user_id is None:
            return await self.get("/user/{user}/trust".format(user=self.token))

    async def trust_user(self, user_id, username):
        """Trust new user."""

        data = {"userName": username}

        return await self.patch("/user/{user}/trust/{user_id}".format(
            user=self.token, user_id=user_id), data=json.dumps(data))

    async def remove_trust(self, user_id):
        """Remove user trust."""

        return await self.delete("/user/{user}/trust/{user_id}".format(
            user=self.token, user_id=user_id))
