import pytest

from cactusbot.api import CactusAPI
from cactusbot.commands.magic import Cube, Temmie
from cactusbot.packets import MessagePacket

cube = Cube(CactusAPI("test_token"))

async def verify_cube(packet, expected):
    _, *args = packet[1:].text.split()
    response = (await cube(*args, username=packet.user, packet=packet))
    if isinstance(response, str):
        assert response == expected
    elif isinstance(response, MessagePacket):
        assert response.text == expected
    else:
        raise TypeError


@pytest.mark.asyncio
async def test_cube():

    await verify_cube(
        MessagePacket("!cube", user="Username"),
        "Username³"
    )

    await verify_cube(
        MessagePacket("!cube 2"),
        "8. Whoa, that's 2Cubed!"
    )

    await verify_cube(
        MessagePacket("!cube a b c d e f g h"),
        ' · '.join([n + '³' for n in "a b c d e f g h".split()])
    )

    await verify_cube(
        MessagePacket("!cube a b c d e f g h i"),
        "Whoa, that's 2 many cubes!"
    )

    await verify_cube(
        MessagePacket("!cube 3 eggs and 4 slices of toast"),
        "27 · eggs³ · and³ · 64 · slices³ · of³ · toast³"
    )

    await verify_cube(
        MessagePacket("!cube lots of taco salad ", ("emoji", "😃")),
        "lots³ · of³ · taco³ · salad³ · 😃³"
    )

temmie = Temmie(CactusAPI("test_token"))


@pytest.mark.asyncio
async def test_temmie():

    await temmie()

    assert (await temmie("hoi")).text == "hOI!!!!!! i'm tEMMIE!!"

    assert not (await temmie("hoi")).action
    assert (await temmie("flakes")).action
