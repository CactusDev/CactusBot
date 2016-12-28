"""Define custom magic commands."""

from .. import Command
from .alias import Alias
from .cactus import Cactus
from .command import Meta
from .config import Config
from .cube import Cube, Temmie
from .quote import Quote
from .repeat import Repeat
from .social import Social
from .trust import Trust
from .uptime import Uptime

COMMANDS = (Alias, Cactus, Meta, Config, Cube, Temmie,
            Quote, Repeat, Social, Trust, Uptime)

__all__ = ("Alias", "Command", "Cactus", "Meta", "Config", "Cube",
           "Temmie", "Quote", "Repeat", "Social", "Trust", "Uptime")
