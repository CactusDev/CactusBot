"""Interact with Beam."""

import json
from os import getcwd
from os import path
from .api import BeamAPI
from .chat import BeamChat
from .liveloading import BeamLiveloading

__all__ = ["BeamAPI", "BeamChat", "BeamLiveloading"]
with open(path.join(path.dirname(__file__), "emotes.json")) as f:
    emotes = json.load(f)
