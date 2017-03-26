"""Config command."""

from .command import Command

VALID_TOGGLE_ON_STATES = ("on", "allow", "enable", "true")
VALID_TOGGLE_OFF_STATES = ("off", "disallow", "disable", "false")


async def _update_deep_config(api, scope, field, section, value):
    """Update a deep section of the config."""

    return await api.update_config({
        scope: {
            field: {
                section: value
            }
        }
    })


async def _update_config(api, scope, field, value):
    """Update a config value."""

    return await api.update_config({
        scope: {
            field: value
        }
    })


async def _get_event_data(api, event):
    """Get data about an event."""

    data = (await (await api.get_config()).json())["data"]
    event = data["attributes"]["announce"][event]
    return event


class Config(Command):
    """Config Command."""

    COMMAND = "config"

    @Command.command(role="moderator")
    class Follow(Command):
        """Follow subcommand."""

        @Command.command(role="moderator", name="follow")
        async def default(self, *value: False):
            """Get status, and message of the follow event, or toggle."""

            value = ' '.join(value)

            if not value:
                data = await _get_event_data(self.api, "follow")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis', message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(self.api, "announce", "follow", "announce", True)
                return "Follow announcements are now enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(self.api, "announce", "follow", "announce", False)
                return "Follow announcements are now disabled."
            else:
                return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the follow message."""

            if not message:
                data = (await (await self.api.get_config()).json())["data"]
                message = data["attributes"]["announce"]["follow"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(self.api, "announce", "follow", "message", ' '.join(message))
            return "Set new follow message response."

    @Command.command(role="moderator")
    class Subscribe(Command):
        """Subcommand subcommand."""

        @Command.command(role="moderator", name="subscribe")
        async def default(self, *value: False):
            """Get status, and message of the subscribe event, or toggle."""

            value = ' '.join(value)

            if not value:
                data = await _get_event_data(self.api, "subscribe")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis', message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(self.api, "announce", "subscribe", "announce", True)
                return "Subscribe announcements are now enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(self.api, "announce", "subscribe", "announce", False)
                return "Subscribe announcements are now disabled."
            else:
                return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the subscribe message."""

            if not message:
                data = (await (await self.api.get_config()).json())["data"]
                message = data["attributes"]["announce"]["subscribe"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(
                self.api, "announce", "subscribe", "message", ' '.join(message))
            return "Set new subscribe message response."

    @Command.command(role="moderator")
    class Host(Command):
        """Host subcommand."""

        @Command.command(role="moderator", name="host")
        async def default(self, *value: False):
            """Get status, and message of the host event, or toggle."""

            value = ' '.join(value)

            if not value:
                data = await _get_event_data(self.api, "host")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis', message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(self.api, "announce", "host", "announce", True)
                return "Host announcements are now enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(self.api, "announce", "host", "announce", False)
                return "Host announcements are now disabled."
            else:
                return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the host message."""

            if not message:
                data = (await (await self.api.get_config()).json())["data"]
                message = data["attributes"]["announce"]["host"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(self.api, "announce", "host", "message", ' '.join(message))
            return "Set new host message response."

    @Command.command(role="moderator")
    class Leave(Command):
        """Leave subcommand."""

        @Command.command(role="moderator", name="leave")
        async def default(self, *value: False):
            """Get status, and message of the leave event, or toggle."""

            value = ' '.join(value)

            if not value:
                data = await _get_event_data(self.api, "leave")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis', message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(self.api, "announce", "leave", "announce", True)
                return "Leave announcements are now enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(self.api, "announce", "leave", "announce", False)
                return "Leave announcements are now disabled."
            else:
                return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the leave message."""

            if not message:
                data = (await (await self.api.get_config()).json())["data"]
                message = data["attributes"]["announce"]["leave"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(self.api, "announce", "leave", "message", ' '.join(message))
            return "Set new leave message response."

    @Command.command(role="moderator")
    class Join(Command):
        """Join subcommand."""

        @Command.command(role="moderator", name="join")
        async def default(self, *value: False):
            """Get status, and message of the join event, or toggle."""

            value = ' '.join(value)

            if not value:
                data = await _get_event_data(self.api, "join")
                return "{dis}abled, message: `{message}`".format(
                    dis='En' if data["announce"] else 'Dis', message=data["message"])

            if value in VALID_TOGGLE_ON_STATES:
                await _update_deep_config(self.api, "announce", "join", "announce", True)
                return "Join announcements are now enabled."
            elif value in VALID_TOGGLE_OFF_STATES:
                await _update_deep_config(self.api, "announce", "join", "announce", False)
                return "Join announcements are now disabled."
            else:
                return "Invalid boolean value: `{}`!".format(value)

        @Command.command(role="moderator")
        async def message(self, *message: False):
            """Set the join message."""

            if not message:
                data = (await (await self.api.get_config()).json())["data"]
                message = data["attributes"]["announce"]["join"]["message"]
                return "Current response: `{}`".format(message)

            await _update_deep_config(self.api, "announce", "join", "message", ' '.join(message))
            return "Set new join message response."

    @Command.command(role="moderator")
    class Spam(Command):
        """Spam subcommand."""

        @Command.command()
        class Urls(Command):
            """Urls subcommand."""

            @Command.command(name="urls")
            async def default(self, *value: False):
                """Amount subcommand."""

                if not value:
                    return ""

                values = ' '.join(value)

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

        # @Command.command()
        # async def amount(self, value: r"\d+"):
        #     """Emoji subcommand."""

        #     await _update_config(
        #         self.api, "spam", "maxEmoji", int(value))

        #     return "Maximum number of emoji is now {value}.".format(
        #         value=value)

        # @Command.command()
        # async def amount(self, value: r"\d+"):
        #     """Caps subcommand."""

        #     await _update_config(
        #         self.api, "spam", "maxCapsScore", int(value))

        #     return "Maximum capitals score is now {value}.".format(
        #         value=value)
