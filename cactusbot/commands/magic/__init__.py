"""Define custom magic commands."""

from .. import Command
from .cactus import Cactus
from .command import Meta
from .cube import Cube, Temmie
from .quote import Quote
from .social import Social
from .trust import Trust
from .uptime import Uptime
from .alias import Alias

COMMANDS = (Cactus, Meta, Quote, Cube, Temmie, Social, Trust, Uptime, Alias)

__all__ = ["Command", "Meta", "Quote", "Cube",
           "Social", "Trust", "Cactus", "Uptime",
           "Alias"]
