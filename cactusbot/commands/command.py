"""The inner workings of the command system."""

from inspect import signature

from functools import wraps

import re

from logging import getLogger


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

    __command__ = None

    def __init__(self, api):
        self.logger = getLogger(__name__)

        self.api = api

        self.regex = {
            "username": r'@?([A-Za-z0-9]{,32})',
            "command": r'!?(.+)'
        }

        if self.__command__ is None:
            self.__command__ = type(self).__name__.lower()

    @staticmethod
    def subcommand(function):
        """Decorate a subcommand."""

        params = list(signature(function).parameters.values())

        @wraps(function)
        async def wrapper(self, *args, **data):
            """Parse subcommand data."""

            args = list(args)

            args_params = tuple(
                p for p in params if p.kind is p.POSITIONAL_OR_KEYWORD)
            star_param = next(
                (p for p in params if p.kind is p.VAR_POSITIONAL), None)

            data_params = tuple(
                p for p in params if p.kind is p.KEYWORD_ONLY)
            kwargs = {p.name: data.get(p.annotation) for p in data_params}

            arg_range = (
                len(tuple(
                    p for p in args_params if p.default is p.empty
                )) + bool(star_param),
                float('inf') if star_param else len(args_params)
            )

            if not arg_range[0] <= len(args) <= arg_range[1]:

                if star_param is not None:
                    args_params += (star_param,)
                syntax = "!{command} {subcommand} {params}".format(
                    command=self.__command__, subcommand=function.__name__,
                    params='<'+'> <'.join(p.name for p in args_params[1:])+'>'
                )

                if len(args) < arg_range[0]:
                    return "Not enough arguments. ({})".format(syntax)
                elif len(args) > arg_range[1]:
                    return "Too many arguments. ({})".format(syntax)

            for index, argument in enumerate(args_params[:len(args)]):
                annotation = argument.annotation
                if annotation is not argument.empty:
                    if isinstance(annotation, str):
                        if annotation.startswith('?'):
                            annotation = self.regex.get(annotation[1:], '')
                        match = re.match('^'+annotation+'$', args[index])
                        if match is None:
                            return "Invalid {type}: '{value}'.".format(
                                type=argument.name, value=args[index])
                        else:
                            groups = match.groups()
                            if len(groups) == 1:
                                args[index] = groups[0]
                            elif len(groups) > 1:
                                args[index] = groups
                    else:
                        self.logger.warning(
                            "Invalid regex: '%s.%s.%s : %s'.",
                            self.__command__, function.__name__,
                            argument.name, annotation
                        )

            return await function(self, *args[1:], **kwargs)

        wrapper.is_subcommand = True

        return wrapper

    async def __call__(self, *args, **data):
        # TODO: default subcommands
        # TODO: user levels
        # TODO: secret subcommands
        subcommand = self._subcommands.get(args[0])
        if subcommand is not None:
            return await self.inject(await subcommand(self, *args, **data), *args, **data)
        return "Invalid argument: '{}'.".format(args[0])

    @staticmethod
    async def inject(response, *args, **data):
        """Inject targets into a response."""

        response = response.replace("%USER%", data.get("username", "%USER%"))

        try:
            response = re.sub(
                r'%ARG(\d+)%',
                lambda match: args[int(match.group(1))],
                response
            )
        except IndexError:
            return "Not enough arguments!"

        response = response.replace("%ARGS%", ' '.join(args))

        # TODO: implement count
        response = response.replace("%COUNT%", "%COUNT%")

        response = response.replace("%CHANNEL%", data.get("channel", "%CHANNEL%"))

        return response
