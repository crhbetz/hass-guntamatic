"""The guntamatic integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

import chardet

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import create_async_httpx_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import get_guntamatic_response
from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]

type GuntamaticConfigEntry = ConfigEntry[GuntamaticDataUpdateCoordinator]  # noqa: F821

_LOGGER: logging.Logger = logging.getLogger(__package__)


def autodetect_encoding(content):
    """Autodetect encoding of text."""

    return chardet.detect(content).get("encoding")


@dataclass
class GuntamaticDataUpdateCoordinatorConfig:
    """Config data for GuntamaticDataUpdateCoordinator."""

    host: str
    name: str
    scan_interval: int = 30


class GuntamaticDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the API."""

    def __init__(
        self, hass: HomeAssistant, config: GuntamaticDataUpdateCoordinatorConfig
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=config.scan_interval),
            update_method=self.update_data,
            always_update=True,
        )
        self.config = config
        self._schedule_refresh()

    async def update_data(self) -> dict[str, Any]:
        """Update data via library."""

        _LOGGER.debug("update_data called")
        try:
            httpx_client = create_async_httpx_client(
                self.hass, default_encoding=autodetect_encoding
            )
            self._schedule_refresh()
            _LOGGER.debug("update_data finished")
            return await get_guntamatic_response(httpx_client, self.config.host)
        except Exception as exception:
            _LOGGER.debug(
                "Failed to update guntamatic data: %s",
                exception,
                exc_info=True,
                stack_info=True,
            )
            raise UpdateFailed(exception) from exception


async def async_setup_entry(hass: HomeAssistant, entry: GuntamaticConfigEntry) -> bool:
    """Set up this integration using UI."""

    _LOGGER.info("Called async_setup_entry in init.py")
    config = GuntamaticDataUpdateCoordinatorConfig(
        entry.data[CONF_HOST], entry.data[CONF_NAME], entry.data[CONF_SCAN_INTERVAL]
    )

    coordinator = GuntamaticDataUpdateCoordinator(hass, config)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _LOGGER.info("Finished async_setup_entry in init.py")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
