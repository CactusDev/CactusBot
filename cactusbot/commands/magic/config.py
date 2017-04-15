"""Config command."""

from .command import Command

VALID_TOGGLE_ON_STATES = ("on", "allow", "enable", "true")
VALID_TOGGLE_OFF_STATES = ("off", "disallow", "disable", "false")


async def _update_deep_config(api, scope, field, section, value):
    """Update a deep section of the config."""

    return await api.config.update({
        scope: {
            field: {
                section: value
            }
        }
    })


async def _update_config(api, scope, field, value):
    """Update a config value."""

    return await api.config.update({
        scope: {
            field: value
        }
    })


async def _get_event_data(api, event):
    """Get data about an event."""

    data = (await (await api.config.get()).json())["data"]
    event = data["attributes"]["announce"][event]
    return event


async def _get_spam_data(api, section):
    """Get data about a section of spam config."""

    data = (await (await api.config.get()).json())["data"]
    spam_section = data["attributes"]["spam"][section]
    return spam_section


class Config(Command):
    """Config Command."""

    COMMAND = "config"

    @Command.command(role="moderator")
    class Follow(Command):
        """Follow subcommand."""

        @Command.command(role="moderator", name="follow")
        async def default(self, value=""):
            """Get status, and message of the follow event, or toggle."""

            if not value:
                data = await _get_event_data(self.api, "follow")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis',
                    message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(
                    self.api, "announce", "follow", "announce", True)
                return "Follow announcements are now enabled."

            if value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(
                    self.api, "announce", "follow", "announce", False)
                return "Follow announcements are now disabled."

            return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the follow message."""

            if not message:
                data = (await (await self.api.config.get()).json())["data"]
                message = data["attributes"]["announce"]["follow"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "follow", "message", ' '.join(message))
            return "Set new follow message response."

    @Command.command(role="moderator")
    class Subscribe(Command):
        """Subcommand subcommand."""

        @Command.command(role="moderator", name="subscribe")
        async def default(self, value=""):
            """Get status, and message of the subscribe event, or toggle."""

            if not value:
                data = await _get_event_data(self.api, "sub")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis',
                    message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(
                    self.api, "announce", "sub", "announce", True)
                return "Subscribe announcements are now enabled."

            if value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(
                    self.api, "announce", "sub", "announce", False)
                return "Subscribe announcements are now disabled."

            return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the subscribe message."""

            if not message:
                data = (await (await self.api.config.get()).json())["data"]
                message = data["attributes"]["announce"]["sub"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "sub", "message", ' '.join(message))
            return "Set new subscribe message response."

    @Command.command(role="moderator")
    class Host(Command):
        """Host subcommand."""

        @Command.command(role="moderator", name="host")
        async def default(self, value=""):
            """Get status, and message of the host event, or toggle."""

            if not value:
                data = await _get_event_data(self.api, "host")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis',
                    message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(
                    self.api, "announce", "host", "announce", True)
                return "Host announcements are now enabled."

            if value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(
                    self.api, "announce", "host", "announce", False)
                return "Host announcements are now disabled."

            return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the host message."""

            if not message:
                data = (await (await self.api.config.get()).json())["data"]
                message = data["attributes"]["announce"]["host"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "host", "message", ' '.join(message))
            return "Set new host message response."

    @Command.command(role="moderator")
    class Leave(Command):
        """Leave subcommand."""

        @Command.command(role="moderator", name="leave")
        async def default(self, value=""):
            """Get status, and message of the leave event, or toggle."""

            if not value:
                data = await _get_event_data(self.api, "leave")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis',
                    message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(
                    self.api, "announce", "leave", "announce", True)
                return "Leave announcements are now enabled."

            if value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(
                    self.api, "announce", "leave", "announce", False)
                return "Leave announcements are now disabled."

            return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the leave message."""

            if not message:
                data = (await (await self.api.config.get()).json())["data"]
                message = data["attributes"]["announce"]["leave"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "leave", "message", ' '.join(message))
            return "Set new leave message response."

    @Command.command(role="moderator")
    class Join(Command):
        """Join subcommand."""

        @Command.command(role="moderator", name="join")
        async def default(self, value=""):
            """Get status, and message of the join event, or toggle."""

            if not value:
                data = await _get_event_data(self.api, "join")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis',
                    message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(
                    self.api, "announce", "join", "announce", True)
                return "Join announcements are now enabled."

            if value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(
                    self.api, "announce", "join", "announce", False)
                return "Join announcements are now disabled."

            return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the join message."""

            if not message:
                data = (await (await self.api.config.get()).json())["data"]
                message = data["attributes"]["announce"]["join"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "join", "message", ' '.join(message))
            return "Set new join message response."

    @Command.command(role="moderator")
    class Spam(Command):
        """Spam subcommand."""

        @Command.command()
        class Urls(Command):
            """Urls subcommand."""

            @Command.command(name="urls")
            async def default(self, value=""):
                """Urls subcommand."""

                if not value:
                    urls = await _get_spam_data(self.api, "allowUrls")
                    return "URLs are {dis}allowed.".format(
                        dis='' if urls else 'dis')

                if value in VALID_TOGGLE_ON_STATES:
                    await _update_config(
                        self.api, "spam", "allowUrls", True)
                    return "URLs are now allowed."

                if value in VALID_TOGGLE_OFF_STATES:
                    await _update_config(
                        self.api, "spam", "allowUrls", False)
                    return "URLs are now disallowed."

                return "Invalid boolean value: '{value}'.".format(value=value)

        @Command.command()
        class Emoji(Command):
            """Emoji subcommand."""

            @Command.command(name="emoji")
            async def default(self, value=""):
                """Emoji subcommand."""

                if not value:
                    emoji = await _get_spam_data(self.api, "maxEmoji")
                    return "Maximum amount of emoji allowed is {}.".format(
                        emoji)

                response = await _update_config(
                    self.api, "spam", "maxEmoji", value)
                if response.status == 200:
                    return "Max emoji updated to {}.".format(value)
                return "An error occurred."

        @Command.command()
        class Caps(Command):
            """Caps subcommand."""

            @Command.command(name="caps")
            async def default(self, value=""):
                """Caps subcommand."""

                if not value:
                    caps = await _get_spam_data(self.api, "maxCapsScore")
                    return "Max caps score is {}.".format(caps)

                response = await _update_config(
                    self.api, "spam", "maxCapsScore", value)
                if response.status == 200:
                    return "Max caps score is now {}.".format(value)
                return "An error occurred."
