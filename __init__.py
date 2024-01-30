# __init__.py
import asyncio
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_EMAIL
from .config_flow import StigaLawnMowerConfigFlow

async def async_setup(hass, config):
    """Set up the Stiga Lawn Mower component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    """Set up Stiga Lawn Mower from a config entry."""
    if "firebase_api_key" in entry.data:
        hass.data[DOMAIN].setdefault("firebase_api_key", entry.data["firebase_api_key"])
        hass.data[DOMAIN].setdefault("clients", {})

    # Load platforms
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # Unload platforms
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Remove Firebase API key from options on unload
    hass.data[DOMAIN].pop("firebase_api_key", None)

    return True