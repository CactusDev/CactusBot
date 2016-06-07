"""The brains of the command system."""

from inspect import signature

from functools import wraps

def subcommand(function):
    """Decorate a subcommand."""

    params = list(signature(function).parameters.values())

    @wraps(function)
    def wrapper(self, *args):
        """Parse subcommand data."""

        args = list(args)

        # TODO: implement function.__doc__
        arg_range = (
            len(tuple(arg for arg in params if arg.default is arg.empty)),
            len(params) if next(
                (p for p in params if p.kind is p.VAR_POSITIONAL), None) else
            float('inf')
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

        # TODO: argument regex
        for index, argument in enumerate(params[:len(args)]):
            annotation = argument.annotation
            if annotation is not argument.empty:
                if callable(annotation):
                    try:
                        args[index] = annotation(args[index])
                    except Exception:
                        return "Invalid {type}: '{value}'.".format(
                            type=annotation.__name__, value=args[index])

        if not params:
            return function(self)

        return function(self, *args[1:])

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

    def __call__(self, *args):
        # TODO: default subcommands
        if args[0] in self._subcommands:
            return self._subcommands[args[0]](self, *args)
        return "Invalid argument: '{}'.".format(args[0])
