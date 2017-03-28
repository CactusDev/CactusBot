"""Test the alias command."""

import pytest

from cactusbot.commands.magic import Alias
from cactusbot.packets import MessagePacket


class MockAPI:
    """Fake API."""

    class Alias:
        async def get(self, command):
            """Get aliases."""

            class Response:
                """Fake API response object."""

                @property
                def status(self):
                    """Response status."""
                    return 200

                def json(self):
                    """Response from the api."""

                    return {
                        "data": {
                            "attributes": {
                                "command": {
                                    "count": 1,
                                    "enabled": True,
                                    "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                    "name": "testing",
                                    "response": {
                                        "action": None,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "commandName": "testing",
                                "name": "test",
                                "token": "Stanley"
                            },
                            "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                            "type": "alias"
                        }
                    }
            return Response()

        async def add(self, command, alias, args=None):
            """Add a new alias."""

            class Response:
                """Fake API response object."""

                @property
                def status(self):
                    """Response status."""
                    return 200

                def json(self):
                    """Response from the api."""
                    return {
                        "data": {
                            "attributes": {
                                "command": {
                                    "count": 1,
                                    "enabled": True,
                                    "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                    "name": "testing",
                                    "response": {
                                        "action": False,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "commandName": "testing",
                                "name": "test",
                                "token": "Stanley"
                            },
                            "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                            "type": "alias"
                        },
                        "meta": {
                            "edited": True
                        }
                    }
            return Response()

        async def remove(self, alias):
            """Remove an alias."""

            class Response:
                """Fake API response."""

                @property
                def status(self):
                    """Response status."""
                    return 200

                def json(self):
                    """JSON response."""
                    return {
                        "meta": {
                            "deleted": [
                                "312ab175-fb52-4a7b-865d-4202176f9234"
                            ]
                        }
                    }
            return Response()
    alias = Alias()
    
    class Command:

        async def get(self):
            """Get all the commands."""

            class Response:
                """Fake API response."""

                @property
                def status(self):
                    """Status of the response."""
                    return 200

                async def json(self):
                    """JSON response."""
                    return {
                        "data": [
                            {
                                "attributes": {
                                    "count": 2,
                                    "enabled": True,
                                    "name": "testing",
                                    "response": {
                                        "action": False,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                "type": "command"
                            },
                            {
                                "attributes": {
                                    "commandName": "testing",
                                    "count": 2,
                                    "enabled": True,
                                    "id": "d23779ce-4522-431d-9095-7bf34718c39d",
                                    "name": "test",
                                    "response": {
                                        "action": False,
                                        "message": [
                                            {
                                                "data": "testing!",
                                                "text": "testing!",
                                                "type": "text"
                                            }
                                        ],
                                        "role": 1,
                                        "target": None,
                                        "user": "Stanley"
                                    },
                                    "token": "Stanley"
                                },
                                "id": "312ab175-fb52-4a7b-865d-4202176f9234",
                                "type": "alias"
                            }
                        ]
                    }
            return Response()
    command = Command()


alias = Alias(MockAPI())


@pytest.mark.asyncio
async def test_create_alias():
    """Create an alias."""
    assert (await alias("add", "test", "testing", packet=MessagePacket(
        "!alias add test testing", role=5))
    ) == "Alias !test for command !testing updated."


@pytest.mark.asyncio
async def test_list_alias():
    """List aliases."""
    assert (await alias("list", packet=MessagePacket(
        "!alias list", role=5))) == "Aliases: test (testing)"


@pytest.mark.asyncio
async def test_remove_alias():
    """Remove an alias."""
    assert (await alias("remove", "test", packet=MessagePacket(
        "!alias remove test", role=5))) == "Alias !test removed."
