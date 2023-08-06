""" Interact with the Healthcheck.io website """
import logging
import asyncio
import socket
import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)

class HealthChecks():
    """ Interact with the Healthcheck.io website """
    def __init__(self, loop=None, ping_url=None, session=None):
        _LOGGER.debug("pyHealthChecks initializing new server at: %s", ping_url)
        self._ping_url = ping_url
        self._loop = loop
        self._session = session
        self._results = False

    def update_url(self, ping_url=None):
        """ Update the url """
        self._ping_url = ping_url

    async def update_connection(self):
        """ Sends the request """
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url=self._ping_url, ssl=False)

                try:
                    if response.status in [200]:
                        self._results = True
                    else:
                        _LOGGER.error(
                            "Error code %s - %s",
                            response.status,
                            response.text,
                        )
                        return None
                except (TypeError, KeyError) as error:
                    _LOGGER.error("Error parsing data from Health Checks, %s", error)
                    return None

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error("Error connecting to Health Checks, %s", error)
            return None

        return self._results
