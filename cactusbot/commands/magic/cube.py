"""Cube things."""


from . import Command

import re


class Cube(Command):
    """Cube things."""

    __command__ = "cube"

    NUMBER_EXPR = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')

    @Command.subcommand
    async def run(self, *args) -> "cube":  # FIXME: make default
        """Cube things!"""

        if args == ('2',):
            return "8! Whoa, that's 2Cubed!"
        elif len(args) > 8:
            return "Whoa! That's 2 many cubes!"

        return ' · '.join(self.cube(arg) for arg in args)

    def cube(self, value: str):
        """Cube a value."""

        if value.startswith(':'):  # HACK: implement better emote parsing
            return '( {} )³'.format(value)

        match = re.match(self.NUMBER_EXPR, value)
        if match is not None:
            return '{:.4g}'.format(float(match.string)**3)

        return '({})³'.format(value)
