"""CactusBot!"""

import logging

import time

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

    def __init__(self, service, *, debug="INFO"):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.service = service

        self.debug = debug  # XXX: find purpose or remove

    async def run(self, username, password):
        """Run bot."""

        self.logger.info(CACTUS_ART)

        # TODO: Add support for multiple services
        try:
            await self.service.run(username, password)

        except KeyboardInterrupt:
            self.logger.info("Removing thorns... done.")

        except Exception:
            self.logger.critical("Oh no, I crashed!", exc_info=True)

            self.logger.info("Restarting in 10 seconds...")

            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.logger.info("CactusBot deactivated.")
