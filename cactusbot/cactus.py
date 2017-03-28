"""CactusBot!"""

import asyncio
import logging

from .sepal import Sepal

__version__ = "v0.4"


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


async def run(api, service, url, *auth):
    """Run bot."""

    logger = logging.getLogger(__name__)
    logger.info(CACTUS_ART)

    await api.login(*api.SCOPES)

    sepal = Sepal(api.token, service, url)

    try:
        await sepal.connect()
        asyncio.ensure_future(sepal.read(sepal.handle))
        await service.run(*auth)

    except KeyboardInterrupt:
        logger.info("Removing thorns... done.")

    except Exception:  # pylint: disable=W0703
        logger.critical("Oh no, I crashed!", exc_info=True)
