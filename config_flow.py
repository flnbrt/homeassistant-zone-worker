"""Config flow for Zone Worker integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN

class ZoneWorkerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zone Worker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Create entry with the provided input
            return self.async_create_entry(title=user_input["room_name"], data=user_input)

        # Schema for user input
        schema = vol.Schema(
            {
                vol.Required("room_name"): str,
                vol.Required("domains", default=["light", "switch"]): vol.All(vol.ensure_list, [str]),
                vol.Optional("include_entities", default=[]): vol.All(vol.ensure_list, [str]),
                vol.Optional("exclude_entities", default=[]): vol.All(vol.ensure_list, [str]),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return ZoneWorkerOptionsFlow(config_entry)


class ZoneWorkerOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Zone Worker."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Save options and return
            return self.async_create_entry(title="", data=user_input)

        # Schema for options
        schema = vol.Schema(
            {
                vol.Required("domains", default=self.config_entry.options.get("domains", ["light", "switch"])):
                    vol.All(vol.ensure_list, [str]),
                vol.Optional("include_entities", default=self.config_entry.options.get("include_entities", [])):
                    vol.All(vol.ensure_list, [str]),
                vol.Optional("exclude_entities", default=self.config_entry.options.get("exclude_entities", [])):
                    vol.All(vol.ensure_list, [str]),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
