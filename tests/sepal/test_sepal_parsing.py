import pytest
from cactusbot.sepal import SepalParser

REPEAT_PACKET = {
    "type": "event",
    "event": "config",
    "channel": "innectic2",
    "data": {
        "message": [
            {
                "text": "Hello! ",
                "data": "Hello! ",
                "type": "text"
            },
            {
                "text": ":D",
                "data": "😮",
                "type": "emoji"
            }
        ]
    }
}

CONFIG_PACKET = {
    "type": "event",
    "event": "config",
    "channel": "innectic2",
    "data": {
        "announce": {
            "follow": {
                "announce": True,
                "message": "Thanks for following, %USER%!"
            },
            "host": {
                "announce": False,
                "message": "Thanks for hosting, %USER%!"
            },
            "join": {
                "announce": False,
                "message": "Hello, %USER%!"
            },
            "leave": {
                "announce": False,
                "message": "Thanks for watching %USER%!"
            },
            "sub": {
                "announce": True,
                "message": "Thanks for subbing, %USER%!"
            }
        },
        "spam": {
            "allowUrls": False,
            "maxCapsScore": 16,
            "maxEmoji": 6
        },
        "token": "innectic2",
        "whitelistedUrls": []
    }
}

parser = SepalParser()


@pytest.mark.asyncio
async def test_parse_repeat():
    packet = await parser.parse_repeat(REPEAT_PACKET)

    assert packet.json["message"] == [
        {
            "text": "Hello! ",
            "data": "Hello! ",
            "type": "text"
        },
        {
            "text": ":D",
            "data": "😮",
            "type": "emoji"
        }
    ]

    assert packet.json["role"] == 1
    assert packet.json["action"] is False
    assert packet.json["target"] is None

    assert packet.text == "Hello! :D"


@pytest.mark.asyncio
async def test_parse_config():

    packets = await parser.parse_config(CONFIG_PACKET)

    assert len(packets) == 3
    announce, spam, urls = packets

    assert announce.json == CONFIG_PACKET["data"]["announce"]
    assert spam.json == CONFIG_PACKET["data"]["spam"]
    assert urls.json == {"urls": CONFIG_PACKET["data"]["whitelistedUrls"]}
