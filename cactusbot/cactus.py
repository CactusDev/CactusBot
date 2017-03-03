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

async def run(api, service, *auth):
    """Run bot."""

    logger = logging.getLogger(__name__)
    logger.info(CACTUS_ART)

    await api.login(*api.SCOPES)

    sepal = Sepal(api.token, service)

    try:
        await sepal.connect()
        asyncio.ensure_future(sepal.read(sepal.handle))
        await service.run(*auth)

    except KeyboardInterrupt:
        logger.info("Removing thorns... done.")

    except Exception:
        logger.critical("Oh no, I crashed!", exc_info=True)

        logger.info("Restarting in 10 seconds...")

        try:
            time.sleep(10)
        except KeyboardInterrupt:
            logger.info("CactusBot deactivated.")
