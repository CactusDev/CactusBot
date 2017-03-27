from hypothesis import strategies as st
from hypothesis import given

from cactusbot.packets import MessagePacket


def test_copy():
    """Test packet copying."""

    initial = MessagePacket("Test message.", user="TestUser")

    copy = initial.copy()
    assert copy.text == "Test message."
    assert copy.user == "TestUser"

    assert initial.copy() is not initial

    new_copy = initial.copy("New message!")
    assert new_copy.text == "New message!"
    assert new_copy.user == "TestUser"


def test_replace():
    """Test packet string replacement."""

    assert MessagePacket("a b c").replace(a='x', b='y').text == "x y c"

    assert MessagePacket("a b c").replace().text == "a b c"

    assert MessagePacket("a b c").replace(b='').text == "a  c"


def test_sub():
    """Test regex substitution."""

    assert MessagePacket("%USER% is great!").sub(
        "%USER%", "Stanley").text == "Stanley is great!"
    assert MessagePacket("I would like 3 ", ("emoji", "😃"), "s.").sub(
        r'\d+', "<number>").text == "I would like <number> 😃s."


def _split(text, *args, **kwargs):
    return [
        component.text for component in
        MessagePacket(text).split(*args, **kwargs)
    ]


def test_split():
    """Test splitting message packets."""

    assert _split("0 1 2 3") == ['0', '1', '2', '3']
    assert _split("0 1 2 3", "2") == ['0 1 ', ' 3']
    assert _split("0 1 2 3", maximum=2) == ['0', '1', '2 3']
    assert _split("0 1 2 3 ") == ['0', '1', '2', '3', '']
    assert _split(" 0 1 2 3") == ['', '0', '1', '2', '3']
    assert _split(" 0 1 2 3 ") == ['', '0', '1', '2', '3', '']


@given(st.text(), st.characters(), st.integers(0, 5))
def test_split_property(text, char, maximum):
    """Test packet splitting using property-based testing."""
    assert _split(text, char, maximum) == text.split(char, maximum)


def test_join():
    """Test joining message packets."""

    assert MessagePacket.join(
        MessagePacket(("text", "I like "), ("emoji", "😃")),
        MessagePacket(" kittens!")
    ).text == "I like 😃 kittens!"

    assert MessagePacket.join(
        MessagePacket("Testing"),
        MessagePacket(" Stuff!")
    ).text == "Testing Stuff!"

    assert MessagePacket.join().text == ""

    assert MessagePacket.join(
        MessagePacket("Hello"),
        MessagePacket("world!"),
        separator="... "
    ).text == "Hello... world!"


@given(st.lists(st.text()), st.characters())
def test_join_property(packets, separator):
    """Test packet joining using property-based testing."""

    assert MessagePacket.join(
        *map(MessagePacket, packets), separator=separator
    ).text == separator.join(packets)
