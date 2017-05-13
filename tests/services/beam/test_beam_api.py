import json

import pytest

from cactusbot.services.beam.api import API, BeamAPI


class FakeResponse:

    def __init__(self, method, endpoint, kwargs):

        self.method = method
        self.endpoint = endpoint
        self.kwargs = kwargs

    async def json(self):

        return self.method, self.endpoint, self.kwargs


@pytest.fixture(autouse=True)
def fake_web_requests(monkeypatch):

    async def request(self, method, endpoint, **kwargs):

        if kwargs.get("raw") is True:
            kwargs.pop("raw")

        else:

            if "data" in kwargs:
                kwargs["data"] = json.loads(kwargs["data"])

            if "headers" in kwargs:
                for key, value in list(kwargs["headers"].items()):
                    if key in self.headers and self.headers[key] == value:
                        kwargs["headers"].pop(key)
                if not kwargs["headers"]:
                    kwargs.pop("headers")

        return FakeResponse(method.upper(), endpoint, kwargs)
    monkeypatch.setattr(API, "request", request)


api = BeamAPI("channel", "token")


@pytest.mark.asyncio
async def test_request():

    assert await (
        await api.request("GET", "/test", headers={"X-Key": "value"}, raw=True)
    ).json() == (
        "GET",
        "/test",
        {
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer token",
                "X-Key": "value"
            }
        }
    )


@pytest.mark.asyncio
async def test_get_bot_channel():

    assert await api.get_bot_channel(fields="id") == (
        "GET",
        "/users/current",
        {"params": {
            "fields": "id"
        }}
    )


@pytest.mark.asyncio
async def test_get_channel():

    assert await api.get_channel("Stanley", fields="userId") == (
        "GET",
        "/channels/Stanley",
        {"params": {
            "fields": "userId"
        }}
    )


@pytest.mark.asyncio
async def test_get_chat():

    assert await api.get_chat("Stanley") == (
        "GET",
        "/chats/Stanley",
        {}
    )


@pytest.mark.asyncio
async def test_update_roles():

    assert await api.update_roles("Potato", ["Banned"], ["Mod"]) == (
        "PATCH",
        "/channels/channel/users/Potato",
        {"data": {
            "add": ["Banned"],
            "remove": ["Mod"]
        }}
    )
