# config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CLIENTS_KEY, FIREBASE_API_KEY
from .stiga_api import StigaApiClient
import logging

_LOGGER = logging.getLogger(__name__)

data_schema = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

class StigaLawnMowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=data_schema,
            )

        if CONF_EMAIL not in user_input or CONF_PASSWORD not in user_input:
            return self.async_show_form(
                step_id="user",
                data_schema=data_schema,
                errors={"base": "invalid_input"},
            )

        email = user_input[CONF_EMAIL]
        password = user_input[CONF_PASSWORD]

        api_client = StigaApiClient(FIREBASE_API_KEY)  # Use your Firebase API Key from const.py

        try:
            firebase_token = await api_client.get_firebase_token(email, password)
            devices = await api_client.get_devices()

            _LOGGER.debug(f"Devices linked to the account: {devices}")

            # Check if the key exists in self.hass.data[DOMAIN]
            if DOMAIN not in self.hass.data:
                self.hass.data[DOMAIN] = {}

            # Store the Stiga API client in self.hass.data[DOMAIN]
            self.hass.data[DOMAIN].setdefault(CLIENTS_KEY, {})
            self.hass.data[DOMAIN][CLIENTS_KEY][self.flow_id] = api_client

            return self.async_create_entry(title="Stiga Integration", data=user_input, options={})
        except Exception as ex:
            _LOGGER.exception(f"Error during login: {ex}")
            return self.async_show_form(step_id="user", errors={"base": "invalid_credentials"})