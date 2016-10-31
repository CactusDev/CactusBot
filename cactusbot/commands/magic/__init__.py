"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote
from .cube import Cube, Temmie
from .social import Social
from .trust import Trust
from.cactus import Cactus

COMMANDS = (Meta, Quote, Cube, Temmie, Social, Trust, Cactus)

__all__ = ["Command", "Meta", "Quote", "Cube", "Trust", "Cactus"]
