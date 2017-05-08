"""Get help with commands."""

import inspect
from numpydoc.docscrape import NumpyDocString
from . import Command, COMMANDS


def _get_summary(raw):
    """Get the summary from the doc string"""
    doc = raw["Summary"]
    return ' '.join(doc)


def _get_arguments(raw):
    """Get the arguments from the doc string"""
    doc = raw["Parameters"]
    return ', '.join("{command}: {description}".format(
        command=param[0], description=' '.join(param[2])) for param in doc)


def _get_example(raw):
    """Get an example from the doc string"""
    doc = raw["Examples"]
    return "{command} gives the output of {response}".format(
        command=doc[0], response=doc[1])

# Mapping for segment arguments to the function
_SEGMENT_MAPPINGS = {
    "": _get_summary,
    "args": _get_arguments,
    "arguments": _get_arguments,
    "example": _get_example
}


class Help(Command):
    """Get help about a command.

    Examples
    --------
    !help help
    Help for `!help`: Get help about a command
    """

    COMMAND = "help"
    ROLE = "moderator"

    @Command.command()
    async def default(self, command_name: "?command", *args: False):
        """Obtain general help about the given command.

        Parameters
        ----------
        command : :obj:`str`
            The command to get the help for

        Examples
        --------
        !help config
        Help for `!config`: Configure the bot to your hearts content.
        """

        segment = ""
        command = [command_name]

        if args:
            # Looking for a subcommand and the segment
            if len(args) > 1:
                for arg in args[:len(args)-1]:
                    command.append(arg)
                potential = args[len(args)-1]
                segment = potential if potential in _SEGMENT_MAPPINGS else ""
            # Only looking for args, or a segment
            else:
                if args[0] in _SEGMENT_MAPPINGS:
                    segment = args[0]
                else:
                    command.append(args[0])

        for registered in COMMANDS:
            if registered.COMMAND == command[0]:
                last = registered
                # Get the lowest subcommand
                for subcommand in command[1:]:
                    checking = last().has_subcommand(subcommand)
                    # Subcommand doesn't exist
                    if checking is None:
                        return "No help available for !{}".format(' '.join(
                            command))
                    last = checking

                # Get the default method, if one exists.
                if inspect.isclass(last):
                    # Attempt to get the default of the class
                    default_last = last().has_subcommand("default")
                    last = default_last if default_last is not None else last
                    #if default_last is not None:
                     #   last = default_last

                    # If there wasn't a default, and there's not a last checked
                    # assume no documentation
                    if default_last is None and last is None:
                        return "No help available for !{}".format(' '.join(
                            command))

                # Get the documentation
                doc = NumpyDocString(last.__doc__)
                command_help = _SEGMENT_MAPPINGS[segment](doc)
                if command_help == "":
                    return "No help available for !{}".format(command_name)
                return "Help for `!{command}`: {help}".format(
                    command=command_name, help=command_help)
        return "Command `!{}` doesn't exist.".format(command_name)
