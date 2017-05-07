"""Manage quotes."""

from aiohttp import get

from . import Command
from ...packets import MessagePacket


class Quote(Command):
    """Manage quotes."""

    COMMAND = "quote"
    ROLE = "moderator"

    @Command.command(hidden=True, role="user")
    async def default(self, quote: r'[1-9]\d*' = None):
        """Get a quote based on ID. If no ID is provided, pick a random one."""

        if quote is None:
            response = await self.api.quote.get()
            data = (await response.json())["data"]
            if not data:
                return "No quotes have been added!"
            return data[0]["attributes"]["quote"]

        response = await self.api.quote.get(quote)
        if response.status == 404:
            return "Quote {} does not exist!".format(quote)
        return (await response.json())["data"]["attributes"]["quote"]

    @Command.command()
    async def add(self, *quote):
        """Add a quote."""
        response = await self.api.quote.add(' '.join(quote))
        data = await response.json()
        return "Added quote #{}.".format(
            data["data"]["attributes"]["quoteId"])

    @Command.command()
    async def edit(self, quote_id: r'[1-9]\d*', *quote):
        """Edit a quote based on ID."""
        response = await self.api.quote.edit(quote_id, ' '.join(quote))
        if response.status == 201:
            return "Added quote #{}.".format(quote_id)
        return "Edited quote #{}.".format(quote_id)

    @Command.command()
    async def remove(self, quote_id: r'[1-9]\d*'):
        """Remove a quote."""
        response = await self.api.quote.remove(quote_id)
        if response.status == 404:
            return "Quote #{} does not exist!".format(quote_id)
        return "Removed quote #{}.".format(quote_id)

    @Command.command(hidden=True)
    async def inspirational(self):
        """Retrieve an inspirational quote."""
        try:
            data = await (await get(
                "http://api.forismatic.com/api/1.0/",
                params=dict(method="getQuote", lang="en", format="json")
            )).json()
        except Exception:  # pylint: disable=W0703
            return MessagePacket(
                "Unable to get an inspirational quote. Have a ",
                ("emoji", "🐹"),
                " instead."
            )
        else:
            return "\"{quote}\" -{author}".format(
                quote=data["quoteText"].strip(),
                author=data["quoteAuthor"].strip() or "Unknown"
            )
