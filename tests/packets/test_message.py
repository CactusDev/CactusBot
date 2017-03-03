from cactusbot.packets import MessagePacket


def _split(text, *args, **kwargs):
    return [
        component.text
        for component in
        MessagePacket(text).split(*args, **kwargs)
    ]


def test_split():

    assert _split("0 1 2 3") == ['0', '1', '2', '3']

    assert _split("0 1 2 3", "2") == ['0 1 ', ' 3']

    assert _split("0 1 2 3", maximum=2) == ['0', '1', '2 3']

    assert _split("0 1 2 3 ") == ['0', '1', '2', '3']
