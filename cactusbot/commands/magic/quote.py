"""Manage quotes."""

from aiohttp import get

from . import Command
from ...packets import MessagePacket


class Quote(Command):
    """Manage quotes."""

    COMMAND = "quote"

    @Command.subcommand(hidden=True)
    async def get(self, quote_id: r'[1-9]\d*'=None):
        """Get a quote based on ID. If no ID is provided, pick a random one."""
        if quote_id is None:
            return MessagePacket(self.api.get_quote())
        return MessagePacket(self.api.get_quote(quote_id))

    @Command.subcommand
    async def add(self, *quote, added_by: "username"):
        """Add a quote."""
        response = await self.api.add_quote(' '.join(quote), added_by=added_by)
        return MessagePacket(
            "Added quote with ID {}.".format(response["data"]["id"])
        )

    @Command.subcommand
    async def remove(self, quote_id: r'[1-9]\d*'):
        """Remove a quote."""
        try:
            self.api.remove_quote(quote_id)
        except Exception:  # FIXME: data, not exceptions
            return MessagePacket("Quote {} does not exist!".format(quote_id))
        else:
            return MessagePacket("Removed quote with ID {}.".format(quote_id))

    @Command.subcommand  # FIXME: make secret
    async def inspirational(self):
        """Retrieve an inspirational quote."""
        try:
            data = await (await get(
                "http://api.forismatic.com/api/1.0/",
                params=dict(method="getQuote", lang="en", format="json")
            )).json()
        except Exception:
            return MessagePacket("Unable to get an inspirational quote.")
        else:
            return MessagePacket("\"{quote}\" -{author}".format(
                quote=data["quoteText"].strip(),
                author=data["quoteAuthor"].strip() or "Unknown"
            ))

    DEFAULT = get
