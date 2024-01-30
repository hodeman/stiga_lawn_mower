# sensor.py
import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CLIENTS_KEY  # Import the DOMAIN and CLIENTS_KEY constants

_LOGGER = logging.getLogger(__name__)

class StigaLawnMowerSensor(Entity):
    def __init__(self, client, robot_uuid, attribute, name):
        self._client = client
        self._robot_uuid = robot_uuid
        self._attribute = attribute
        self._name = name
        self._state = None

    @property
    def name(self):
        return f"{self._name} {self._attribute.capitalize()}"

    @property
    def unique_id(self):
        return f"{self._robot_uuid}_{self._attribute}"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._robot_uuid)},
            "name": self._name,
            "manufacturer": "Stiga",
            "model": "Robotic Lawn Mower",
        }

    async def async_update(self):
        _LOGGER.debug(f"Updating {self._attribute} for {self._name}.")
        try:
            if self._attribute == "battery_level":
                self._state = await self._client.get_battery_level(self._robot_uuid)
            else:
                # Add logic for other attributes if needed
                pass
        except Exception as ex:
            _LOGGER.error(f"Error updating {self._attribute} for {self._name}: {ex}")
            self._state = None

async def async_setup_entry(hass, config_entry, async_add_entities):
    clients = hass.data[DOMAIN].get(CLIENTS_KEY, {})
    for client_id, client in clients.items():
        try:
            devices = await client.get_devices()
            _LOGGER.debug(f"Successfully logged in for client {client_id}. Devices: {devices}")
            for device in devices:
                async_add_entities([
                    StigaLawnMowerSensor(client, device.get("uuid", ""), "battery_level", device.get("name", ""))
                    # Add other sensors if needed
                ])
        except Exception as ex:
            _LOGGER.error(f"Error getting devices for client {client_id}: {ex}")
