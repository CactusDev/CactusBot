"""Magic command internals (and magic)."""

import inspect
import re


class Command:
    """Parent class to all commands."""

    default = None

    api = None

    def __init__(self, api=None):

        if api is not None:
            type(self).api = api

    async def __call__(self, *args, **meta):

        commands = self.commands()
        assert self.default is None or callable(self.default)

        if args:
            command, *arguments = args
            if command in commands:
                try:
                    return await self._run_safe(
                        commands[command], *arguments, **meta)
                except IndexError as error:
                    if error.args[0] == 0:
                        has_default = hasattr(commands[command], "default")
                        has_commands = hasattr(commands[command], "commands")
                        if not (has_default or has_commands):
                            return "Not enough arguments. <{0}>".format(
                                '> <'.join(arg.name for arg in error.args[1]))
                        response = "Not enough arguments. <{0}>".format(
                            '|'.join(
                                commands[command].commands(hidden=False).keys()
                            ))
                        if commands[command].default is not None:
                            try:
                                return await self._run_safe(
                                    commands[command].default,
                                    *arguments, **meta)
                            except IndexError:
                                return response
                        return response
                    else:
                        return "Too many arguments."

        if self.default is not None:
            try:
                return await self._run_safe(self.default, *args, **meta)
            except IndexError:
                pass

        if args:
            command, *_ = args
            return "Invalid argument: '{0}'.".format(command)

        return "Not enough arguments. <{0}>".format(
            '|'.join(self.commands(hidden=False).keys()))

    @classmethod
    def command(cls, name=None, **meta):
        """Accept arguments for command decorator."""

        def decorator(function):
            """Decorate a command."""

            function.COMMAND_META = meta

            if inspect.isclass(function):
                COMMAND = getattr(function, "COMMAND", None)
                function = function(cls.api)
                function.__name__ = function.__class__.__name__
                if COMMAND is not None:
                    function.COMMAND = COMMAND

            if name is not None:
                assert ' ' not in name, "Command name may not contain spaces"
                if getattr(function, "COMMAND", name) is not name:
                    raise NameError("Multiple command name declarations")
                function.COMMAND = name
            elif getattr(function, "COMMAND", None) is None:
                function.COMMAND = function.__name__.lower()

            return function

        return decorator

    async def _run_safe(self, function, *args, **meta):
        self._check_safe(function, *args)

        args = await self._clean_args(function, *args)
        if isinstance(args, str):
            return args
        kwargs = self._clean_kwargs(function, **meta)
        return await function(*args, **kwargs)

    @staticmethod
    def _check_safe(function, *args):

        params = inspect.signature(function).parameters.values()

        pos_args = tuple(
            p for p in params if p.kind is p.POSITIONAL_OR_KEYWORD)
        star_arg = next(
            (p for p in params if p.kind is p.VAR_POSITIONAL), None)

        arg_range = (
            len(tuple(
                p for p in pos_args if p.default is p.empty
            )) + (bool(star_arg) if star_arg and star_arg.annotation else 0),
            len(args) if star_arg else len(pos_args)
        )

        if not arg_range[0] <= len(args) <= arg_range[1]:

            if star_arg is not None:
                pos_args += (star_arg,)

            raise IndexError(len(args) > arg_range[0], pos_args)
        return True

    @staticmethod
    async def _clean_args(function, *args):

        params = inspect.signature(function).parameters.values()

        pos_args = tuple(
            p for p in params if p.kind is p.POSITIONAL_OR_KEYWORD)

        args = list(args)

        for index, arg in enumerate(pos_args[:len(args)]):
            if arg.annotation is not arg.empty:
                error_response = "Invalid {type}: '{value}'.".format(
                    type=arg.name, value=args[index])
                if isinstance(arg.annotation, str):
                    annotation = arg.annotation
                    if annotation.startswith('?'):
                        if annotation == "?command":
                            annotation = r"!?\w{1,32}"
                    match = re.match('^' + annotation + '$', args[index])
                    if match is None:
                        return error_response
                    else:
                        groups = match.groups()
                        if len(groups) == 1:
                            args[index] = groups[0]
                        elif len(groups) > 1:
                            args[index] = groups
                elif callable(arg.annotation):
                    try:
                        args[index] = await arg.annotation(args[index])
                    except Exception:
                        return error_response
                else:
                    raise TypeError("Invalid annotation: {0}".format(
                        arg.annotation))

        return args

    @staticmethod
    def _clean_kwargs(function, **meta):

        params = inspect.signature(function).parameters.values()
        meta_args = (p for p in params if p.kind is p.KEYWORD_ONLY)
        return {p.name: meta.get(p.annotation) for p in meta_args}

    def commands(self, **meta):
        """Return commands belonging to the parent class."""

        disallowed = ["commands", "__class__"]
        return {
            method.COMMAND: method for attr in dir(self)
            if attr not in disallowed
            for method in (getattr(self, attr),)
            if hasattr(method, "COMMAND") and
            all(method.COMMAND_META.get(key, value) == value
                for key, value in meta.items())
        }
