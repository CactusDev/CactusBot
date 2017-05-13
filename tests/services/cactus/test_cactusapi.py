import json

import pytest

from cactusbot.api import CactusAPI


@pytest.fixture(autouse=True)
def fake_web_requests(monkeypatch):

    async def request(self, method, endpoint, **kwargs):

        if "data" in kwargs:
            kwargs["data"] = json.loads(kwargs["data"])

        if method.upper() == "GET" and kwargs.get("is_json") is False:
            kwargs.pop("is_json")
        elif kwargs.get("is_json") is True:
            kwargs.pop("is_json")

        return method.upper(), endpoint, kwargs
    monkeypatch.setattr(CactusAPI, "request", request)


api = CactusAPI("token", "password")


class TestAlias:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.alias.get("tato") == (
            "GET",
            "/user/token/alias/tato",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.alias.add("potato", "tato") == (
            "PATCH",
            "/user/token/alias/tato",
            {"data": {
                "commandName": "potato"
            }}
        )

        assert await api.alias.add("potato", "tato", ["arg"]) == (
            "PATCH",
            "/user/token/alias/tato",
            {"data": {
                "commandName": "potato",
                "arguments": ["arg"]
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):

        assert await api.alias.remove("tato") == (
            "DELETE",
            "/user/token/alias/tato",
            {}
        )


class TestCommand:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.command.get() == (
            "GET",
            "/user/token/command",
            {}
        )

        assert await api.command.get("hoi") == (
            "GET",
            "/user/token/command/hoi",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.command.add("hoi", ["i'm", "temmie"], user_level=4) == (
            "PATCH",
            "/user/token/command/hoi",
            {"data": {
                "response": ["i'm", "temmie"],
                "userLevel": 4
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):

        assert await api.command.remove("hoi") == (
            "DELETE",
            "/user/token/command/hoi",
            {}
        )

    @pytest.mark.asyncio
    async def test_toggle(self):

        assert await api.command.toggle("hoi", False) == (
            "PATCH",
            "/user/token/command/hoi",
            {"data": {
                "enabled": False
            }}
        )

    @pytest.mark.asyncio
    async def test_update_count(self):

        assert await api.command.update_count("hoi", 123) == (
            "PATCH",
            "/user/token/command/hoi/count",
            {"data": {
                "count": 123
            }}
        )


class TestConfig:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.config.get() == (
            "GET",
            "/user/token/config",
            {}
        )

        assert await api.config.get("key1", "key2") == (
            "GET",
            "/user/token/config",
            {"data": {
                "keys": ["key1", "key2"]
            }}
        )

    @pytest.mark.asyncio
    async def test_update(self):

        assert await api.config.update({"key": "value"}) == (
            "PATCH",
            "/user/token/config",
            {"data": {
                "key": "value"
            }}
        )


class TestQuote:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.quote.get() == (
            "GET",
            "/user/token/quote",
            {"params": {
                "random": "true"
            }}
        )

        assert await api.quote.get(8) == (
            "GET",
            "/user/token/quote/8",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.quote.add("This is a quote!") == (
            "POST",
            "/user/token/quote",
            {"data": {
                "quote": "This is a quote!"
            }}
        )

    @pytest.mark.asyncio
    async def test_edit(self):

        assert await api.quote.edit(8, "This is a great quote!") == (
            "PATCH",
            "/user/token/quote/8",
            {"data": {
                "quote": "This is a great quote!"
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):

        assert await api.quote.remove(8) == (
            "DELETE",
            "/user/token/quote/8",
            {}
        )


class TestRepeat:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.repeat.get() == (
            "GET",
            "/user/token/repeat",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.repeat.add("hoi", 60) == (
            "PATCH",
            "/user/token/repeat/hoi",
            {"data": {
                "commandName": "hoi",
                "period": 60
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):
        assert await api.repeat.remove("hoi") == (
            "DELETE",
            "/user/token/repeat/hoi",
            {}
        )


class TestSocial:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.social.get() == (
            "GET",
            "/user/token/social",
            {}
        )

        assert await api.social.get("github") == (
            "GET",
            "/user/token/social/github",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.social.add("github", "github.com/CactusDev") == (
            "PATCH",
            "/user/token/social/github",
            {"data": {
                "url": "github.com/CactusDev"
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):

        assert await api.social.remove("github") == (
            "DELETE",
            "/user/token/social/github",
            {}
        )


class TestTrust:

    @pytest.mark.asyncio
    async def test_get(self):

        assert await api.trust.get() == (
            "GET",
            "/user/token/trust",
            {}
        )

        assert await api.trust.get(12345) == (
            "GET",
            "/user/token/trust/12345",
            {}
        )

    @pytest.mark.asyncio
    async def test_add(self):

        assert await api.trust.add(95845, "Stanley") == (
            "PATCH",
            "/user/token/trust/95845",
            {"data": {
                "userName": "Stanley"
            }}
        )

    @pytest.mark.asyncio
    async def test_remove(self):

        assert await api.trust.remove(12345) == (
            "DELETE",
            "/user/token/trust/12345",
            {}
        )
