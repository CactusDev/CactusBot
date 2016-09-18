class Handler(object):
    def __init__(self, name: str, action: int, is_async: bool=False):
        """
        Arguments:
            name: str       Used by CB to enable/disable plugins by name
            action: int     Part of the message handling process that this
                                handler affects
            is_async: bool  Can this function be run async, or does it require
                                data in a certain state & does it have to be
                                executed at a certain time
        """
        self.NAME = name
        self.ACTION = action
        self.IS_ASYNC = is_async

    async def run(self):
        """Runs the handler."""
        raise NotImplementedError
