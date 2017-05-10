import pytest
from tests.api import MockAPI

from cactusbot.handlers import EventHandler
from cactusbot.packets import EventPacket

event_handler = EventHandler({
    "cache_follow": True,
    "cache_host": True,
    "cache_join": True,
    "cache_leave": True,
    "cache_time": 1200
}, MockAPI("test_token", "test_password"))


@pytest.mark.asyncio
async def test_on_message():

    assert (await event_handler.on_start(
        None
    )).text == "CactusBot activated. 🌵"


@pytest.mark.asyncio
async def test_on_follow():

    assert (await event_handler.on_follow(EventPacket(
        "follow", "TestUser"
    ))).text == "Thanks for the follow, TestUser!"

    assert (await event_handler.on_follow(EventPacket(
        "follow", "TestUser", success=False
    ))) is None

    event_handler.alert_messages["follow"]["announce"] = False

    assert await event_handler.on_follow(EventPacket("follow", "TestUser")) is None


@pytest.mark.asyncio
async def test_on_subscribe():

    assert (await event_handler.on_subscribe(EventPacket(
        "subscribe", "TestUser"
    ))).text == "Thanks for the subscription, TestUser!"

    event_handler.alert_messages["subscribe"]["announce"] = False

    assert await event_handler.on_subscribe(EventPacket("subscribe", "TestUser")) is None


@pytest.mark.asyncio
async def test_on_host():

    assert (await event_handler.on_host(EventPacket(
        "host", "TestUser"
    ))).text == "Thanks for the host, TestUser!"

    event_handler.alert_messages["host"]["announce"] = False

    assert await event_handler.on_host(EventPacket("leave", "TestUser")) is None


@pytest.mark.asyncio
async def test_on_join():

    assert await event_handler.on_join(EventPacket("join", "TestUser")) is None

    event_handler.alert_messages["join"]["announce"] = True

    assert (await event_handler.on_join(EventPacket(
        "join", "TestUser"
    ))).text == "Welcome, TestUser!"


@pytest.mark.asyncio
async def test_on_leave():

    assert await event_handler.on_leave(EventPacket("leave", "TestUser")) is None

    event_handler.alert_messages["leave"]["announce"] = True

    assert (await event_handler.on_leave(EventPacket(
        "leave", "TestUser"
    ))).text == "Thanks for watching, TestUser!"
