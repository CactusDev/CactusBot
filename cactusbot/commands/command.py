# pylint: skip-file

"""Magic command internals (and magic)."""

import inspect
import re

ROLES = {
    5: "Owner",
    4: "Moderator",
    2: "Subscriber",
    1: "User",
    0: "Banned"
}

REGEXES = {
    "command": r"!?([\w-]{1,32})"
}


class Command:
    """Parent class to all magic commands.

    Function definitions may use annotations to specify information about the
    arguments.

    Using a string signifies a required regular expression to match. (If no
    groups are specified, the entire match is returned. If one group is
    specified, it is returned as a string. Otherwise, the tuple of groups is
    returned.)

    Special shortcuts, beginning with a `?`, are taken from a built-in list.

        =============   ===================
        Shortcut        Regular Expression
        =============   ===================
        ``?command``    ``!?([\\w-]{1,32})``
        =============   ===================

    Using the ``False`` annotation on `*args` signifies that no arguments are
    required to successfully execute the command.

    An asynchronous function may be used as a validation annotation, as well.
    The function is passed the command argument. If an exception is not raised,
    the return value of the function is passed to the command. Otherwise, an
    error message is returned.

    Keyword-only arguments should be annotated with the requested metadata.

        =========   =======================================================
        Value       Description
        =========   =======================================================
        username    The username of the message sender.
        channel     The name of the channel which the message was sent in.
        packet      The entire :obj:`MessagePacket`.
        =========   =======================================================

    The ``COMMAND`` attribute is required, and should be set to the command
    name string.

    Parameters
    ----------
    api : :obj:`CactusAPI` or :obj:`None`
        Instance of :obj:`CactusAPI`. Must be provided to the top-level magic
        :obj:`Command`.

    Examples
    --------
    >>> class Test(Command):
    ...
    ...     COMMAND = "test"
    ...
    ...     @Command.command()
    ...     async def add(self, command: "?command", *response):
    ...         return "Added !{command} with response {response}.".format(
    ...             command=command, response=' '.join(response))
    ...
    ...     @Command.command(hidden=True)
    ...     async def highfive(self, *, recipient: "username"):
    ...         return "Have a highfive, {recipient}!".format(
    ...             recipient=recipient)
    ...
    ...     @Command.command()
    ...     async def potato(self, *users: False):
    ...
    ...         if not users:
    ...             return "Have a potato!"
    ...
    ...         return "Have a potato, {users}!".format(users=', '.join(users))


    """

    default = None

    api = None

    def __init__(self, api=None):

        if api is not None:
            self.api = api
            Command.api = api

    async def __call__(self, *args, **meta):

        commands = self.commands()
        assert self.default is None or callable(self.default)

        if args:

            command, *arguments = args

            if command in commands:

                role = commands[command].COMMAND_META.get("role", 1)

                if isinstance(role, str):
                    role = list(ROLES.keys())[list(map(
                        str.lower, ROLES.values())).index(role.lower())]
                if "packet" in meta and meta["packet"].role < role:
                    return "Role level '{role}' or higher required.".format(
                        role=ROLES[max(k for k in ROLES.keys() if k <= role)])

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
        """Accept arguments for command decorator.


        Parameters
        ----------
        name : :obj:`str` or :obj:`None`, default :obj:`None`
            The name of the command. If :obj:`None`, the function name is used.
        hidden : :obj:`bool`
            Whether or not to hide the command from help messages.
        role : :obj:`str` or :obj:`int`, default ``1``
            The minimum role required to run the command.
            String capitalization is ignored.
        **meta
            Custom meta filters. Any keyword arguments are valid.

            =======   ===========
            Number    String
            =======   ===========
            5         Owner
            4         Moderator
            2         Subscriber
            1         User
            0         Banned
            =======   ===========

        Returns
        -------
        :obj:`function`
            Decorator command.

        Examples
        --------
        >>> @Command.command()
        ... async def hello():
        ...     return "Hello, world."

        >>> @Command.command(name="return")
        ... async def return_():
        ...     return "Achievement Get: Return to Sender"

        >>> @Command.command(hidden=True)
        ... async def secret():
        ...     return "Wow, you found a secret!"

        >>> @Command.command(role="moderator")
        ... async def secure():
        ...     return "Moderator-only things have happened."
        """

        def decorator(function):
            """Decorate a command."""

            function.COMMAND_META = meta

            if inspect.isclass(function):
                COMMAND = getattr(function, "COMMAND", None)
                function = function(Command.api)
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
                        assert annotation[1:] in REGEXES, "Invalid shortcut"
                        annotation = REGEXES[annotation[1:]]
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
        """Return commands belonging to the parent class.

        Parameters
        ----------
        **meta
            Attributes to filter by.

        Returns
        -------
        :obj:`dict`
            Commands which match the meta attributes.
            Keys are names, values are methods.

        Examples
        --------
        >>> @Command.command()
        ... class Test(Command):
        ...
        ...     @Command.command()
        ...     async def simple(self):
        ...         return "Simple response."
        ...
        ...     @Command.command(hidden=True)
        ...     async def secret(self):
        ...         return "#secrets"
        ...
        >>> Test.commands(hidden=False).keys()
        dict_keys(['simple'])
        """

        disallowed = ["commands", "__class__"]
        return {
            method.COMMAND: method for attr in dir(self)
            if attr not in disallowed
            for method in (getattr(self, attr),)
            if hasattr(method, "COMMAND") and
            all(method.COMMAND_META.get(key, value) == value
                for key, value in meta.items())
        }
