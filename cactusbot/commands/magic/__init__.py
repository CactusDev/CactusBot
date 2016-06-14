"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote
from .cube import Cube

COMMANDS = (Meta, Quote, Cube)

__all__ = ["Command", "Meta", "Quote", "Cube"]
