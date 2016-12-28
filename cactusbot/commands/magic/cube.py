"""Cube things."""

import random
import re
from difflib import get_close_matches

from . import Command
from ...packets import MessagePacket


class Cube(Command):
    """Cube things."""

    COMMAND = "cube"

    NUMBER_EXPR = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')

    @Command.command(hidden=True)
    async def default(self, *args: False, username: "username", raw: "packet"):
        """Cube things!"""

        if not args:
            return self.cube(username)
        if args == ('2',):
            return "8. Whoa, that's 2Cubed!"
        elif len(args) > 8:
            return "Whoa, that's 2 many cubes!"

        result = []

        for component in raw.split(maximum=1)[1]:
            if component.type == "text":
                if component.text.split():
                    result += self.join(
                        map(self.cube, component.text.split()), ' · ')
                    result.append(' · ')
            else:
                result.append(component)
                result.append('³')
                result.append(' · ')

        return MessagePacket(*result[:-1])

    def cube(self, value: str):
        """Cube a value."""

        match = re.match(self.NUMBER_EXPR, value)
        if match is not None:
            return '{:.4g}'.format(float(match.string)**3)
        return '{}³'.format(value)

    @staticmethod
    def join(iterable, delimeter):
        iterable = iter(iterable)
        yield next(iterable)
        for item in iterable:
            yield delimeter
            yield item


@Command.command()
class Temmie(Command):
    "awwAwa!!"

    COMMAND = "temmie"

    QUOTES = (
        ("fhsdhjfdsfjsddshjfsd", False),
        ("hOI!!!!!! i'm tEMMIE!!", False),
        ("awwAwa cute!! (pets u)", False),
        ("OMG!! humans TOO CUTE (dies)", False),
        ("NO!!!!! muscles r... NOT CUTE", False),
        ("NO!!! so hungr... (dies)", False),
        ("FOOB!!!", False),
        ("can't blame a BARK for tryin'...", False),
        ("RATED TEM OUTTA TEM. Loves to pet cute humans. "
         "But you're allergic!", True),
        ("Special enemy Temmie appears here to defeat you!!", True),
        ("Temmie is trying to glomp you.", True),
        ("Temmie forgot her other attack.", True),
        ("Temmie is doing her hairs.", True),
        ("Smells like Temmie Flakes.", True),
        ("Temmie vibrates intensely.", True),
        ("Temmiy accidentally misspells her own name.", True),
        ("You flex at Temmie...", True),
        ("Temmie only wants the Temmie Flakes.", True),
        ("You say hello to Temmie.", True)
    )

    @Command.command(hidden=True)
    async def default(self, *query: False):
        """hOI!!!!!!"""

        if query:
            quotes = dict(zip((
                quote.lower() for quote, _ in self.QUOTES), self.QUOTES))
            lowered = get_close_matches(
                ' '.join(query).lower(), quotes.keys(), n=1, cutoff=0)[0]
            quote, action = quotes[lowered]
        else:
            quote, action = random.choice(self.QUOTES)

        return MessagePacket(quote, action=action)
