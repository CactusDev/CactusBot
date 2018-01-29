"""Magic command internals (and magic)."""

import inspect
import re

ROLES = {
    5: "Owner",
    4: "ChannelEditor",
    4: "Moderator",
    2: "Subscriber",
    1: "User",
    0: "Banned"
}

REGEXES = {
    "command": r"!?([\w-]{1,32})"
}


class ArgsError(Exception):
    """Error raised when an unexpected number of arguments was received.

    Parameters
    ----------
    direction : :obj:`bool`
        Whether there were too many (:obj:`True`) or too few (:obj:`False`)
        arguments passed.
    args : :obj:`tuple` of :obj:`inspect.Parameter` s
        :obj:`tuple` of the method's positional or keyword arguments.
    """

    def __init__(self, direction, args):

        super().__init__()

        self.direction = direction
        self.args = args


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

    ROLE = "user"

    def __init__(self, api=None):

        if api is not None:
            self.api = api
            Command.api = api

    async def __call__(self, *args, **meta):
        # pylint: disable=R0911

        commands = self.commands()
        assert self.default is None or callable(self.default)

        if args and args[0] in commands:

            command, *arguments = args

            to_run = [commands[command]]
            if getattr(commands[command], "default", None) is not None:
                to_run.append(commands[command].default)

            for index, running in enumerate(to_run):
                try:
                    return await self._run_safe(running, *arguments, **meta)

                except ArgsError as error:

                    if index > 0:
                        continue

                    if error.direction:
                        return "Too many arguments."

                    has_default = hasattr(running, "default")
                    has_commands = hasattr(running, "commands")
                    if not (has_default or has_commands):
                        return "Not enough arguments. {0}".format(
                            ' '.join(map(self._display, error.args)))

            keys = commands[command].commands(hidden=False).keys()

            if keys and list(keys) != ["default"]:
                return "Not enough arguments. <{0}>".format('|'.join(keys))

            param_args = self._check_safe(
                commands[command].default, *arguments, error=False)

            return "Not enough arguments. {0}".format(' '.join(map(
                self._display, param_args
            )))

        if self.default is not None:
            try:
                return await self._run_safe(self.default, *args, **meta)
            except ArgsError as err:
                error = err

        if args:
            return "Invalid argument: '{0}'.".format(args[0])

        if self.default is not None:
            return "Not enough arguments. {0}".format(
                ' '.join(map(self._display, error.args)))

        return "Not enough arguments. <{0}>".format(
            '|'.join(self.commands(hidden=False).keys()))

    @staticmethod
    def _display(arg):

        # pylint: disable=W0212

        if arg._kind is arg.VAR_POSITIONAL:

            if arg.annotation is False:
                syntax = "[{}...]"
            else:
                syntax = "<{}...>"

        elif arg.default is inspect._empty:
            syntax = "<{}>"

        else:
            syntax = "[{}]"

        argument_name = arg.name
        if argument_name == "_":
            argument_name = "argument"
        return syntax.format(argument_name)

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
                command = getattr(function, "COMMAND", None)
                function = function(Command.api)
                function.__name__ = function.__class__.__name__
                if command is not None:
                    function.COMMAND = command

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

        role = function.COMMAND_META.get("role", self.ROLE)

        if isinstance(role, str):
            role = list(ROLES.keys())[list(map(
                str.lower, ROLES.values())).index(role.lower())]

        if "packet" in meta and meta["packet"].role < role:
            # pylint: disable=C0201
            return "Role level '{r}' or higher required.".format(
                r=ROLES[max(k for k in ROLES.keys() if k <= role)])

        self._check_safe(function, *args)

        args = await self._clean_args(function, *args)
        if isinstance(args, str):
            return args
        kwargs = self._clean_kwargs(function, **meta)
        return await function(*args, **kwargs)

    @staticmethod
    def _check_safe(function, *args, error=True):

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

        if star_arg is not None:
            pos_args += (star_arg,)

        if error and not arg_range[0] <= len(args) <= arg_range[1]:
            raise ArgsError(len(args) > arg_range[0], pos_args)

        return pos_args

    @staticmethod
    async def _clean_args(function, *args):

        params = inspect.signature(function).parameters.values()

        pos_args = tuple(
            p for p in params if p.kind is p.POSITIONAL_OR_KEYWORD)

        args = list(args)

        for index, arg in enumerate(pos_args[:len(args)]):
            if arg.annotation is not arg.empty:
                argument_name = arg.name.replace('_', ' ')
                error_response = "Invalid '{type}': '{value}'.".format(
                    type=argument_name, value=args[index])
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
                    except Exception:  # pylint: disable=W0703
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

        disallowed = ["commands", "api", "__class__"]

        return {  # pylint: disable=E1101
            method.COMMAND: method
            for attr in dir(self)
            if attr not in disallowed
            for method in (getattr(self, attr),)
            if hasattr(method, "COMMAND") and
            all(method.COMMAND_META.get(key, value) == value
                for key, value in meta.items())
        }
