"""Config flow for Zone Worker integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers import config_validation as cv  # Config validation helpers
from .const import DOMAIN
import logging

# Define the logger instance
_LOGGER = logging.getLogger(__name__)

class ZoneWorkerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zone Worker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        errors = {}

        if user_input is not None:
            # Log the user input for debugging purposes
            _LOGGER.debug("User input received in config flow: %s", user_input)

            # Create the config entry
            return self.async_create_entry(title=user_input["room"], data=user_input)

        # Define the configuration schema
        schema = vol.Schema({
            vol.Required("room", default="Living Room"): str,
            vol.Required("domains", default=["light", "switch"]): vol.All(cv.ensure_list, [str]),
            vol.Optional("include", default=[]): vol.All(cv.ensure_list, [str]),
            vol.Optional("exclude", default=[]): vol.All(cv.ensure_list, [str]),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

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
            # Convert comma-separated strings to lists before saving
            user_input["domains"] = [domain.strip() for domain in user_input["domains"].split(",")]
            user_input["include_entities"] = [
                entity.strip() for entity in user_input["include_entities"].split(",") if entity.strip()
            ]
            user_input["exclude_entities"] = [
                entity.strip() for entity in user_input["exclude_entities"].split(",") if entity.strip()
            ]
            return self.async_create_entry(title="", data=user_input)

        # Prepare current options
        options = self.config_entry.options
        default_domains = ",".join(options.get("domains", ["light", "switch"]))
        default_include = ",".join(options.get("include_entities", []))
        default_exclude = ",".join(options.get("exclude_entities", []))

        # Schema for options
        schema = vol.Schema(
            {
                vol.Required("domains", default=default_domains): str,  # Comma-separated string
                vol.Optional("include_entities", default=default_include): str,  # Comma-separated string
                vol.Optional("exclude_entities", default=default_exclude): str,  # Comma-separated string
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
