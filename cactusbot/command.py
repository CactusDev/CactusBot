"""The brains of the command system."""

from inspect import signature

from functools import wraps

import re

from logging import getLogger


def subcommand(function):
    """Decorate a subcommand."""

    names = list(signature(function).parameters.keys())
    params = list(signature(function).parameters.values())

    @wraps(function)
    def wrapper(self, *args):
        """Parse subcommand data."""

        if not params:
            return function(self)

        args = list(args)

        star = bool(
            next((p for p in params if p.kind is p.VAR_POSITIONAL), False)
        )

        arg_range = (
            len(tuple(arg for arg in params if arg.default is arg.empty)),
            float('inf') if star else len(params)
        )

        if not arg_range[0] <= len(args) <= arg_range[1]:

            syntax = "!{command} {subcommand} {params}".format(
                command=self.__command__, subcommand=function.__name__,
                params='<{}>'.format('> <'.join(p.name for p in params[1:]))
            )

            if len(args) < len(params):
                return "Not enough arguments. ({})".format(syntax)
            elif len(args) > len(params):
                return "Too many arguments. ({})".format(syntax)

        for index, argument in enumerate(params[:len(args)]):
            annotation = argument.annotation
            if annotation is not argument.empty:
                if isinstance(annotation, str):
                    if re.match('^'+annotation+'$', args[index]) is None:
                        return "Invalid {type}: '{value}'.".format(
                            type=argument.name, value=args[index])
                else:
                    self.logger.warning(
                        "Invalid regex: '%s.%s.%s : %s'.",
                        self.__command__, function.__name__,
                        argument.name, annotation
                    )

        positional = len(names) - star
        return function(
            self, *args[positional:],
            **dict(zip(names[1:positional], args[1:positional]))
        )

    wrapper.is_subcommand = True

    return wrapper


class CommandMeta(type):
    """Manage the backend of commands via a metaclass."""

    def __new__(mcs, name, bases, attrs):
        subcommands = {}
        for value in attrs.values():
            if getattr(value, "is_subcommand", None):
                subcommands[value.__name__] = value
        attrs["_subcommands"] = subcommands
        return super().__new__(mcs, name, bases, attrs)


class Command(metaclass=CommandMeta):
    """Parent all command classes."""

    def __init__(self):
        self.logger = getLogger(__name__)

    def __call__(self, *args):
        # TODO: default subcommands
        if args[0] in self._subcommands:
            return self._subcommands[args[0]](self, *args)
        return "Invalid argument: '{}'.".format(args[0])
