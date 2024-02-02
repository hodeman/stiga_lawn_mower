# stiga_api.py
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class StigaApiClient:
    BASE_URL = "https://connectivity-production.stiga.com/api"

    def __init__(self, firebase_api_key, api_host="connectivity-production.stiga.com"):
        self.firebase_api_key = firebase_api_key
        self._firebase_token = None
        self.api_host = api_host

    async def authenticate(self, email, password):
        # ... (existing authenticate method)

    async def get_devices(self):
        _LOGGER.debug("Getting devices.")
        if not self._firebase_token:
            raise Exception("Firebase token is not available.")

        url = f"{self.BASE_URL}/garage/integration"
        headers = {
            "Authorization": f"Bearer {self._firebase_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    data = await response.json()

                    if response.status == 200:
                        devices = data.get("data", [])
                        _LOGGER.debug(f"Devices retrieved: {devices}")
                        return devices
                    else:
                        _LOGGER.error(f"Failed to get devices. Status code: {response.status}")
                        raise Exception(f"Failed to get devices. Status code: {response.status}")
        except Exception as e:
            _LOGGER.error(f"Error getting devices: {e}")
            raise
