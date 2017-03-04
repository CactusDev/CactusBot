from cactusbot.packets import MessagePacket


def _split(text, *args, **kwargs):
    return [
        component.text
        for component in
        MessagePacket(text).split(*args, **kwargs)
    ]


def test_sub():
    """Test regex substitution."""

    assert MessagePacket("%USER% is great!").sub(
        "%USER%", "Stanley").text == "Stanley is great!"
    assert MessagePacket("I would like 3 ", ("emoji", "😃"), "s.").sub(
        r'\d+', "<number>").text == "I would like <number> 😃s."


def test_split():
    """Test splitting message packets."""

    assert _split("0 1 2 3") == ['0', '1', '2', '3']
    assert _split("0 1 2 3", "2") == ['0 1 ', ' 3']
    assert _split("0 1 2 3", maximum=2) == ['0', '1', '2 3']
    assert _split("0 1 2 3 ") == ['0', '1', '2', '3']
    assert _split(" 0 1 2 3") == ['0', '1', '2', '3']
    assert _split(" 0 1 2 3 ") == ['0', '1', '2', '3']


def test_join():
    """Test joining message packets."""

    packet1 = MessagePacket(("text", "I like "), ("emoji", "😃"))
    packet2 = MessagePacket(" kittens!")

    assert MessagePacket.join(packet1, packet2).text == "I like 😃 kittens!"

    packet1 = MessagePacket("Testing")
    packet2 = MessagePacket(" Stuff!")

    assert MessagePacket.join(packet1, packet2).text == "Testing Stuff!"
