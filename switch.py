import logging
import requests
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_OFF, STATE_ON

_LOGGER = logging.getLogger(__name__)

DOMAIN = "stiga_lawn_mower"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Stiga Lawn Mower switch platform."""
    async_add_entities([StigaLawnMowerSwitch()])


class StigaLawnMowerSwitch(SwitchEntity):
    """Representation of a Stiga Lawn Mower switch."""

    def __init__(self):
        self._state = STATE_OFF

    @property
    def name(self):
        """Return the name of the switch."""
        return "Stiga Lawn Mower"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state == STATE_ON

    def turn_on(self, **kwargs):
        """Turn on the switch."""
        self._send_command("startsession")

    def turn_off(self, **kwargs):
        """Turn off the switch."""
        self._send_command("endsession")

    def _send_command(self, command):
        """Send command to Stiga API."""
        try:
            # Replace 'YOUR_FIREBASE_TOKEN' with the actual token obtained from authentication
            headers = {"Authorization": "Bearer YOUR_FIREBASE_TOKEN"}
            url = f"https://connectivity-production.stiga.com/api/devices/YOUR_DEVICE_UUID/command/{command}"
            response = requests.post(url, headers=headers)

            if response.status_code == 200:
                self._state = STATE_ON if command == "startsession" else STATE_OFF
            else:
                _LOGGER.error(f"Failed to send command. Status code: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Error sending command: {e}")
