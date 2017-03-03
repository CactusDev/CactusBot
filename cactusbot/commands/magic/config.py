"""Config command."""

from .command import Command

VALID_TOGGLE_ON_STATES = ("on", "allow", "enable", "true")
VALID_TOGGLE_OFF_STATES = ("off", "disallow", "disable", "false")


async def _update_config(api, scope, field, section, value):
    return await api.update_config({
        scope: {
            field: {
                section: value
            }
        }
    })

async def _update_spam_config(api, scope, field, value):
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
                await _update_config(self.api, "announce", "follow", "announce", True)
                return "Follow announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "follow", "announce", False)
                return "Follow announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

        @Command.command()
        async def subscribe(self, value):
            """Subscribe subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "subscribe", "announce", True)
                return "Subscribe announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "subscribe", "announce", False)
                return "Subscribe announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

        @Command.command()
        async def host(self, value):
            """Host subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "host", "announce", True)
                return "Host announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "host", "announce", False)
                return "Host announcements are disabled."
            else:
                return "Invalid boolean value: '{value}'".format(value=value)

        @Command.command()
        async def leave(self, value):
            """Leave subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "leave", "announce", True)
                return "Leave announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "leave", "announce", False)
                return "Leave announcements are disabled."

        @Command.command()
        async def join(self, value):
            """Join subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_config(self.api, "announce", "join", "announce", True)
                return "Join announcements are enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_config(self.api, "announce", "join", "announce", False)
                return "Join announcements are disabled."

    @Command.command(role="moderator")
    class Spam(Command):
        """Spam subcommand."""

        @Command.command()
        async def urls(self, value):
            """Urls subcommand."""

            if value in VALID_TOGGLE_ON_STATES:
                await _update_spam_config(
                    self.api, "spam", "allowUrls", True)
                return "URLs are now allowed."

            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_spam_config(
                    self.api, "spam", "allowUrls", False)
                return "URLs are now disallowed."

            else:
                return "Invalid boolean value: '{value}'.".format(value=value)

        @Command.command()
        async def emoji(self, value: r"\d+"):
            """Emoji subcommand."""

            await _update_spam_config(
                self.api, "spam", "maxEmoji", int(value))

            return "Maximum number of emoji is now {value}.".format(
                value=value)

        @Command.command()
        async def caps(self, value: r"\d+"):
            """Caps subcommand."""

            await _update_spam_config(
                self.api, "spam", "maxCapsScore", int(value))

            return "Maximum capitals score is now {value}.".format(
                value=value)
