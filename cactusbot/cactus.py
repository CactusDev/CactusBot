"""CactusBot!"""

import asyncio
import logging

from .sepal import Sepal

__version__ = "v0.4.1-dev"


CACTUS_ART = r"""CactusBot initialized!

         --`
   `     /++/- `
   o+:.  :+osy -/:.`
   oo+o/ /osyy -+///`
   /shh+ +oo+/ ./ooo`
   //+o+ /+osy /soo+`
   ++//- :oyhy /hyo+`
   /+oo/ /+/// -+/++`
    .:+/ ://++ :+///`
         :+ooo :oo+-
         +o++/ --`
         +o+oo
         -ohhy
           `:+     CactusBot {version}

Made by: 2Cubed, Innectic, and ParadigmShift3d
""".format(version=__version__)


class CactusBot:
    """CactusBot instance."""

    def __init__(self, api, service, url):

        self.api = api
        self.service = service
        self.sepal = Sepal(api.token, service, url)

        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        await self.api.__aenter__()
        await self.sepal.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.api.__aexit__(*args, **kwargs)
        await self.sepal.__aexit__(*args, **kwargs)
        await self.service.__aexit__(*args, **kwargs)

    async def run(self, *auth):
        """Run bot."""

        self.logger.info(CACTUS_ART)

        await self.api.login(*self.api.SCOPES)

        await self.sepal.connect()
        asyncio.ensure_future(self.sepal.read(self.sepal.handle))
        await self.service.run(*auth)
