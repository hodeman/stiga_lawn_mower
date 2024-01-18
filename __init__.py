import logging
import requests

from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "stiga_lawn_mower"
PLATFORMS = ["sensor"]

async def async_setup(hass, config):
    """Set up the Stiga Lawn Mower component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up Stiga Lawn Mower from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Extract necessary information from the config entry
    api_key = entry.data["api_key"]
    email = entry.data["email"]
    password = entry.data["password"]

    # Fetch Firebase Bearer Token
    firebase_token = await fetch_firebase_token(api_key, email, password)
    if not firebase_token:
        _LOGGER.error("Failed to retrieve Firebase Bearer Token")
        return False

    # Save the Firebase Bearer Token in the data dictionary
    hass.data[DOMAIN][entry.entry_id] = {"firebase_token": firebase_token}

    # Set up the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def fetch_firebase_token(api_key, email, password):
    """Fetch Firebase Bearer Token."""
    url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = await async_get_clientsession().post(
            url, params={"key": api_key}, json=payload, headers=headers
        )
        response.raise_for_status()
        data = await response.json()

        if "idToken" in data:
            return data["idToken"]
        else:
            _LOGGER.error("Authentication error: %s", data.get("error", {}).get("message"))
            return None

    except requests.RequestException as error:
        _LOGGER.error("Network error: %s", error)
        return None
