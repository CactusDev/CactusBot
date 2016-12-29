import pytest

from cactusbot.api import CactusAPI
from cactusbot.commands.magic import Cactus

cactus = Cactus(CactusAPI("test_token"))


@pytest.mark.asyncio
async def test_default():
    assert (await cactus()).text == "Ohai! I'm CactusBot! 🌵"


@pytest.mark.asyncio
async def test_docs():
    assert (await cactus("docs")).text == ("Check out my documentation at "
                                           "cactusbot.rtfd.org.")


@pytest.mark.asyncio
async def test_twitter():
    assert (await cactus("twitter")).text == (
        "You can follow the team behind CactusBot at: "
        "twitter.com/CactusDevTeam")


@pytest.mark.asyncio
async def test_github():
    assert (await cactus("github")).text == (
        "Check out my GitHub repository at: github.com/CactusDev/CactusBot")
    assert (await cactus("github", "cactusbot")).text == (
        "Check out my GitHub repository at: github.com/CactusDev/CactusBot")
    assert (await cactus("github", "CactusDev")).text == (
        "Check out the CactusDev GitHub organization at: github.com/CactusDev")
    assert (await cactus("github", "issue")).text == (
        "Create a GitHub issue at: github.com/CactusDev/CactusBot/issues")
    assert (await cactus("github", "CactusAPI")).text == (
        "Check out the GitHub repository for CactusAPI at: "
        "github.com/CactusDev/CactusAPI")
    assert (await cactus("github", "SEPAL")).text == (
        "Check out the GitHub repository for Sepal at: "
        "github.com/CactusDev/Sepal")
    assert (await cactus("github", "assets")).text == (
        "Check out the CactusDev assets at: github.com/CactusDev/CactusAssets")
    assert (await cactus("github", "nonexistant")).text == (
        "Unknown project 'nonexistant'.")


@pytest.mark.asyncio
async def test_help():
    assert (await cactus("help")) == (
        "Try our docs (!cactus docs). "
        "If that doesn't help, tweet at us (!cactus twitter)!")
