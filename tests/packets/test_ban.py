"""Test the ban packet."""

from cactusbot.packets import BanPacket


def test_ban_packet():

    packet = BanPacket("TestUser")

    assert packet.duration == 0
    assert packet.user == "TestUser"


def test_str():
    assert str(BanPacket("Stanley")) == "<Ban: Stanley>"
    assert str(BanPacket("Stanley", 5)) == "<Ban: Stanley, 5 seconds>"


def test_json():

    assert BanPacket("Stanley", 5).json == {
        "user": "Stanley",
        "duration": 5
    }
