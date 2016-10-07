"""Cube things."""

import re

from random import choice
from difflib import get_close_matches

from . import Command
from ...packets import MessagePacket
from ...services.beam.parser import BeamParser


class Cube(Command):
    """Cube things."""

    COMMAND = "cube"

    NUMBER_EXPR = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')

    @Command.subcommand(hidden=True)
    def run(self, *args: False, username: "username") -> "cube":
        """Cube things!"""

        if not args:
            return self.cube(username)
        if args == ('2',):
            return MessagePacket(
                ("text", "8. Woah, that's 2Cubed!"), user="BOT USER")
        elif len(args) > 8:
            return MessagePacket(
                    ("text", "Woah, that's 2 many cubes"), user="BOT USER")

        return ' · '.join(self.cube(arg) for arg in args)

    def cube(self, value: str):
        """Cube a value."""

        if value.startswith(':'):  # HACK: global emote parsing required
            return '{} ³'.format(value)

        match = re.match(self.NUMBER_EXPR, value)
        if match is not None:
            return MessagePacket(
                ("text", '{:.4g}'.format(float(match.string)**3)),
                user="BOT USER")
        return MessagePacket(("text", '({})³'.format(value)), user="BOT USER")

    DEFAULT = run


class Temmie(Command):
    "awwAwa!!"

    COMMAND = "temmie"

    quotes = [
        "fhsdhjfdsfjsddshjfsd",
        "hOI!!!!!! i'm tEMMIE!!",
        "awwAwa cute!! (pets u)",
        "OMG!! humans TOO CUTE (dies)",
        "NO!!!!! muscles r... NOT CUTE",
        "NO!!! so hungr... (dies)",
        "FOOB!!!",
        "can't blame a BARK for tryin'...",
        ("/me RATED TEM OUTTA TEM. Loves to pet cute humans. "
         "But you're allergic!"),
        "/me Special enemy Temmie appears here to defeat you!!",
        "/me Temmie is trying to glomp you.",
        "/me Temmie forgot her other attack.",
        "/me Temmie is doing her hairs.",
        "/me Smells like Temmie Flakes.",
        "/me Temmie vibrates intensely.",
        "/me Temmiy accidentally misspells her own name.",
        "/me You flex at Temmie...",
        "/me Temmie only wants the Temmie Flakes.",
        "/me You say hello to Temmie."
    ]  # HACK: using /me, which is not global

    @Command.subcommand(hidden=True)
    def get(self, query=None):
        """hOI!!!!!!"""
        if query is None:
            return MessagePacket(
                ("text", choice(self.quotes)),
                user="BOT USER"
            )
        return MessagePacket(
            ("text", get_close_matches(query, self.quotes, n=1, cutoff=0)[0]),
            user="BOT USER"
        )

    DEFAULT = get
