"""The Home Assistant Zone Worker integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the Zone Worker component."""
    _LOGGER.info("Setting up Zone Worker")

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zone Worker from a config entry."""
    _LOGGER.info(f"Setting up Zone Worker entry: {entry.data}")
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.info(f"Unloading Zone Worker entry: {entry.data}")
    await hass.config_entries.async_forward_entry_unload(entry, "switch")
    return True
