"""CactusBot!"""

import asyncio
import logging
import time

from .sepal import Sepal

__version__ = "v0.4-dev"


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


class Cactus:
    """Run CactusBot safely."""

    def __init__(self, services):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.services = services

    async def run(self, api):
        """Run bot."""

        self.logger.info(CACTUS_ART)

        await api.login(*api.SCOPES)

        try:
            for service in self.services:
                sepal = Sepal(api.token, service)
                await sepal.connect()

                asyncio.ensure_future(sepal.read(sepal.handle))
                await service.run()

        except KeyboardInterrupt:
            self.logger.info("Removing thorns... done.")

        except Exception:
            self.logger.critical("Oh no, I crashed!", exc_info=True)

            self.logger.info("Restarting in 10 seconds...")

            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.logger.info("CactusBot deactivated.")
