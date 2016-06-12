"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote

COMMANDS = (Meta, Quote)

__all__ = ["Command", "Meta", "Quote"]
