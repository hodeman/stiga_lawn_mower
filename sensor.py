"""Sensor platform for Stiga Lawn Mower integration."""
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from .stiga_api import StigaApiClient

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_client = StigaApiClient(config_entry.data["email"], config_entry.data["password"])
    devices = api_client.get_devices()

    sensors = []
    for device in devices:
        sensors.append(StigaLawnMowerSensor(api_client, device))

    async_add_entities(sensors, True)

class StigaLawnMowerSensor(Entity):
    def __init__(self, api_client, device):
        self.api_client = api_client
        self.device = device

    async def async_update(self):
        # Implement logic to update sensor data from Stiga API
        # For example, use self.api_client to get the latest data for the device
        # Update self._state with the new data
        pass

    @property
    def name(self):
        return f"Stiga {self.device['name']} Status"

    @property
    def state(self):
        return self._state
