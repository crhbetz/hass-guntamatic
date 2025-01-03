"""Guntamatic API Client."""

import logging
from typing import Any

from httpx import AsyncClient, codes

_LOGGER: logging.Logger = logging.getLogger(__name__)


class APIError(Exception):
    """General API error."""


async def get_guntamatic_response(client: AsyncClient, host: str) -> dict[str, Any]:
    """Get data from the API."""

    url_mapping = f"http://{host}/daqdesc.cgi"
    url_data = f"http://{host}/daqdata.cgi"

    _LOGGER.debug("Getting mapping from guntamatic at %s", url_mapping)
    mapping = await client.get(url_mapping)
    _LOGGER.debug("Mapping from guntamatic: %s", mapping)

    _LOGGER.debug("Getting data from guntamatic at %s", url_data)
    data = await client.get(url_data)
    _LOGGER.debug("Data from guntamatic: %s", data)

    if mapping.status_code != codes.OK or data.status_code != codes.OK:
        _LOGGER.warning("Get_guntamatic_response got non-2xx response from %s", host)
        return None

    parsed: dict = {}
    for description, value in zip(
        mapping.text.splitlines(), data.text.splitlines(), strict=True
    ):
        if "reserved" in description:
            continue
        if "Störung" in description:
            if str(value).strip() == "":
                value = "0"
        try:
            name, unit = description.split(";")
        except ValueError:
            _LOGGER.warning("ValueError: Unable to split description: %s", description)
            continue
        parsed[name] = {"value": value.strip(), "unit": unit.strip()}

    if parsed != {}:
        _LOGGER.debug("get_guntamatic_response returning parsed data: %s", parsed)
        return parsed
    return None
