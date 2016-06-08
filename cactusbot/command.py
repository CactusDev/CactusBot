"""The brains of the command system."""

from inspect import signature

from functools import wraps

import re

from logging import getLogger


def subcommand(function):
    """Decorate a subcommand."""

    params = list(signature(function).parameters.values())

    @wraps(function)
    def wrapper(self, *args, **data):
        """Parse subcommand data."""

        if not params:
            return function(self)

        args = list(args)

        args_params = tuple(
            p for p in params if p.kind is p.POSITIONAL_OR_KEYWORD)
        star_param = next(
            (p for p in params if p.kind is p.VAR_POSITIONAL), None)

        data_params = tuple(
            p for p in params if p.kind is p.KEYWORD_ONLY)
        kwargs = dict((p.name, data.get(p.annotation)) for p in data_params)


        arg_range = (
            len(tuple(p for p in args_params[1:] if p.default is p.empty)),
            float('inf') if star_param else len(args_params)-1
        )

        if not arg_range[0] <= len(args) <= arg_range[1]:

            syntax = "!{command} {subcommand} {params}".format(
                command=self.__command__, subcommand=function.__name__,
                params='<'+'> <'.join(p.name for p in args_params[1:])+'>'
            )

            if len(args) < len(args_params):
                return "Not enough arguments. ({})".format(syntax)
            elif len(args) > len(args_params):
                return "Too many arguments. ({})".format(syntax)

        for index, argument in enumerate(args_params[:len(args)]):
            annotation = argument.annotation
            if annotation is not argument.empty:
                if isinstance(annotation, str):
                    match = re.match('^'+annotation+'$', args[index])
                    if match is None:
                        return "Invalid {type}: '{value}'.".format(
                            type=argument.name, value=args[index])
                    elif match.groups():
                        args[index] = match.group(1)
                else:
                    self.logger.warning(
                        "Invalid regex: '%s.%s.%s : %s'.",
                        self.__command__, function.__name__,
                        argument.name, annotation
                    )

        return function(
            self, *args[1:],
            **kwargs
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

    def __call__(self, *args, **data):
        # TODO: default subcommands
        # TODO: user levels
        if args[0] in self._subcommands:
            return self._subcommands[args[0]](self, *args, **data)
        return "Invalid argument: '{}'.".format(args[0])
