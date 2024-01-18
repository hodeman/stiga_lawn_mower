import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import aiohttp_client

_LOGGER = logging.getLogger(__name__)

DOMAIN = "stiga_lawn_mower"

class StigaLawnMowerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # Validate the user's input
            # Add additional validation if necessary
            if not user_input.get(CONF_EMAIL) or not user_input.get(CONF_PASSWORD):
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "invalid_credentials"},
                )

            # Fetch Firebase Bearer Token
            firebase_token = await self.fetch_firebase_token(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])
            if not firebase_token:
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "authentication_failed"},
                )

            # Add the configuration entry
            return self.async_create_entry(
                title="Stiga Lawn Mower Integration",
                data={"firebase_token": firebase_token},
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
            }),
        )

    async def fetch_firebase_token(self, email, password):
        """Fetch Firebase Bearer Token."""
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
        api_key = "AlzaSyCPtRBU_hwWZYsguHp9ucGrfNac0kXR6ug"  # Your Firebase API Key

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }

        try:
            response = await aiohttp_client.async_get_clientsession(self.hass).post(
                url, params={"key": api_key}, json=payload, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = await response.json()

            if "idToken" in data:
                return data["idToken"]
            else:
                _LOGGER.error("Authentication error: %s", data.get("error", {}).get("message"))
                return None

        except aiohttp_client.errors.ClientResponseError as error:
            _LOGGER.error("Network error: %s", error)
            return None
