"""Test the trust command."""

import pytest

from cactusbot.api import CactusAPI
from cactusbot.commands.magic import Trust
from cactusbot.packets import MessagePacket

# trust = Trust(CactusAPI("test_token", "test_password"))


class MockAPI:
    """Fake api."""

    async def get_trust(self, user_id=None):
        """Get trusts."""

        class Response:
            """Fake API response object."""
            @property
            def status(self):
                """Response status."""
                return 200

            async def json(self):
                """JSON version of the response."""

                if user_id:
                    return {
                        "data": {
                            {
                                "attributes": {
                                    "token": "TestChannel",
                                    "userId": "95845",
                                    "userName": "Stanley"
                                }
                            }
                        }
                    }
                else:
                    return {
                        "data": [
                            {
                                "attributes": {
                                    "token": "TestChannel",
                                    "userId": "95845",
                                    "userName": "Stanley"
                                }
                            }
                        ]
                    }
        return Response()

    async def add_trust(self, user_id, username):
        """Add a new trust."""
        class Response:
            """Fake API response object."""
            @property
            def status(self):
                """Response status."""
                return 200

            async def json(self):
                """JSON response."""
                return {
                    "attributes": {
                        "attributes": {
                            "token": "TestChannel",
                            "userId": "95845",
                            "userName": "Stanley"
                        },
                        "id": "7875b898-fbb3-426f-aca3-7375d97326b0",
                        "type": "trust"
                    },
                    "meta": {
                        "created": True
                    }
                }
        return Response()

    async def remove_trust(self, user_id):
        """Remove a trust."""
        class Response:
            """Fake API response."""
            @property
            def status(self):
                """Response status."""
                return 200

            async def json(self):
                """JSON response."""
                return {
                    "meta": {
                        "deleted": [
                            "7875b898-fbb3-426f-aca3-7375d97326b0"
                        ]
                    }
                }
        return Response()

trust = Trust(MockAPI())

@pytest.mark.asyncio
async def test_trust_list():
    """Get a list of trusts."""
    assert (await trust("list")) == "Trusted users: Stanley."

@pytest.mark.asyncio
async def test_trust_add():
    """Add a new trust."""
    assert (await trust("add", "Stanley")).text == "User Stanley has been trusted."

@pytest.mark.asyncio
async def test_trust_remove():
    """Remove a trust."""
    assert (await trust("remove", "Stanley")).text == "Removed trust for user Stanley."

@pytest.mark.asyncio
async def test_trust_toggle():
    """Toggle a trust."""
    assert (await trust("Stanley")).text == "Stanley is no longer trusted."
