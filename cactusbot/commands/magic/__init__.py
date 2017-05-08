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
from .multi import Multi

COMMANDS = [Alias, Cactus, Meta, Config, Cube, Temmie,
            Quote, Repeat, Social, Trust, Uptime, Multi]

# HACK?: Disabling this is required, because the only way for the !help command
# to get a list of the commands, is if the COMMANDS variable already exists.

# pylint: disable=C0413
from .help import Help
COMMANDS.append(Help)

__all__ = ("Alias", "Command", "Cactus", "Meta", "Config", "Cube",
           "Temmie", "Quote", "Repeat", "Social", "Trust", "Uptime",
           "Multi", "Help")
