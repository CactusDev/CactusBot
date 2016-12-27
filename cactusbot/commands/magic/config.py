"""Config command."""

from .command import Command


@Command.command()
class Config(Command):
    """Config command"""

    COMMAND = "config"

    @Command.command()
    async def announce(self, attribute=None, *args: False):
        """Announce subcommand."""

        if attribute is None:
            return "You must supply an attribute!"

        if not args:
            return "You must supply a message!"

        if attribute.lower() not in ["follow", "subscribe", "host"]:
            return "Invalid announcement type. Available: follow, subscribe, host"
        else:
            message = ' '.join(args)

            response = await self.api.update_config({"announce": {attribute: {"message": message}}})
            if response.status == 200:
                return "Updated announcment"

    @Command.command()
    async def spam(self, attribute=None, *args: False):
        """Spam subcommand."""

        if attribute is None:
            return "You must supply an attribute!"

        if not args:
            return "You must supply a value!"

        if attribute.lower() not in ["links", "emoji"]:
            return "Invalid spam type. Available: links, emoji"
        else:
            translations = {
                "links": "allowLinks",
                "emoji": "maxEmoji"
            }

            action = None
            if attribute.lower() == "links":
                if args[0] in ["false", "disable", "off"]:
                    action = False
                elif args[0] in ["true", "enable", "on"]:
                    action = True
                else:
                    return "Invalid action. Available: on/true/enable, off/false/disable"
            elif attribute.lower() == "emoji":
                try:
                    action = int(args[0])
                except ValueError:
                    return "Amount must be a number."

            if action or not action:
                response = await self.api.update_config(
                    {"spam": {translations[attribute.lower()]: action}})
                if response.status == 200:
                    return "{} updated.".format(translations[attribute.lower()].title())
