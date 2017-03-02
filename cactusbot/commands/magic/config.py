"""Config command."""

from .command import Command

VALID_TOGGLE_ON_STATES = ("on", "allow", "enable", "true")
VALID_TOGGLE_OFF_STATES = ("off", "disallow", "disable", "false")


async def _update_config(api, scope, field, value):
    return await api.update_config({
        scope: {
            field: value
        }
    })


class Config(Command):
    """Config command"""

    COMMAND = "config"

    @Command.command(role="moderator")
    class Announce(Command):
        """Announce sub command."""

        @Command.command()
        async def follow(self, value):
            """Follow subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "follow", True)
                return "Follow announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "follow", False)
                return "Follow announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

        @Command.command()
        async def subscribe(self, value):
            """Subscribe subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "subscribe", True)
                return "Subscribe announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "subscribe", False)
                return "Subscribe announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

        @Command.command()
        async def host(self, value):
            """Host subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "host", True)
                return "Host announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "host", False)
                return "Host announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

    @Command.command(role="moderator")
    class Spam(Command):
        """Spam subcommand."""

        @Command.command()
        async def urls(self, value):
            """Urls subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(
                    self.api, "spam", "allowUrls", True)
                return "URLs are now allowed."

            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(
                    self.api, "spam", "allowUrls", False)
                return "URLs are now disallowed."

            else:
                return "Invalid boolean value: '{value}'.".format(value=value)

        @Command.command()
        async def emoji(self, value: r"\d+"):
            """Emoji subcommand."""

            await _update_config(
                self.api, "spam", "maxEmoji", int(value))

            return "Maximum number of emoji is now {value}.".format(
                value=value)

        @Command.command()
        async def caps(self, value: r"\d+"):
            """Caps subcommand."""

            await _update_config(
                self.api, "spam", "maxCapsScore", int(value))

            return "Maximum capitals score is now {value}.".format(
                value=value)

    @Command.command()
    class Whitelist(Command):
        """Whitelist subcommand."""

        @Command.command()
        async def url(self, url):
            """Whitelist a url in chat."""

            await _update_config(
                self.api, "spam", "whitelistedUrls", url
            )

            return "Added {url} to the whitelist.".format(url=url)

        @Command.command()
        async def word(self, word):
            """Whitelist a word in chat."""

            await _update_config(
                self.api, "spam", "whitelistedWords", word
            )

            return "Added {word} to the whitelist.".format(word=word)
