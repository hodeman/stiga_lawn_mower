"""
Stiga Lawn Mower integration for Home Assistant
"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "stiga_lawn_mower"

# List of platforms to support. There should be a matching .py file for each platform in the same folder.
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

# This is the list of all of the platforms that Stiga Lawn Mower integrates with.  In your case, it's just 'sensor'.
async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Stiga Lawn Mower component."""
    # No configuration is needed. Return True to indicate successful setup.
    return True

# This is an example of async_setup_entry that is called when the configuration entry is setup during integration setup.
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Stiga Lawn Mower from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Call the setup function for each platform (in your case, just 'sensor').
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Call the unload function for each platform (in your case, just 'sensor').
    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, platform)

    return True
