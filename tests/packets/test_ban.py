"""Test the ban packet."""

from cactusbot.packets import BanPacket

def test_ban_packet():
    packet = BanPacket("TestUser")

    assert packet.duration == 0
    assert packet.user == "TestUser"
