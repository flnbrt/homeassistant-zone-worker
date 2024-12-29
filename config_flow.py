"""Config flow for Zone Worker integration."""
from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class ZoneWorkerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zone Worker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=user_input["room_name"], data=user_input)

        schema = vol.Schema(
            {
                vol.Required("room_name"): str,
                vol.Required("domains", default=["light", "switch"]): vol.All(cv.ensure_list, [str]),
                vol.Optional("include_entities", default=[]): vol.All(cv.ensure_list, [str]),
                vol.Optional("exclude_entities", default=[]): vol.All(cv.ensure_list, [str]),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
