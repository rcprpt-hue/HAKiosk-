import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from .const import DOMAIN, DEFAULT_PORT, CONF_DEVICE_ID

class HAKioskConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Clean host: remove http:// or https:// and trailing slashes
            host = user_input[CONF_HOST].replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
            user_input[CONF_HOST] = host
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Tablet Entrada"): str,
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Required(CONF_DEVICE_ID): str,
            }),
            errors=errors,
        )
