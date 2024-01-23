import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "stiga_lawn_mower"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

async def validate_input(hass, data):
    # Implement the logic to validate the provided credentials
    # Return True if valid, False otherwise
    return True

class StigaLawnMowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Stiga Lawn Mower."""

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            if await validate_input(self.hass, user_input):
                return self.async_create_entry(title="Stiga Lawn Mower", data=user_input)
            else:
                errors["base"] = "invalid_credentials"

        data_schema = {
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema), errors=errors)
