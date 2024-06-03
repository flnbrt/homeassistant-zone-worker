"""Config flow for Zone Worker integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers import selector
from homeassistant.helpers.area_registry import async_get as async_get_area_registry
from .const import DOMAIN

class ZoneWorkerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zone Worker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input["include_area"], data=user_input)

        area_registry = async_get_area_registry(self.hass)
        areas = area_registry.async_list_areas()
        area_options = {area.id: area.name for area in areas}

        data_schema = vol.Schema({
            vol.Required("include_area"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=list(area_options.values()), multiple=False)
        ),
            vol.Optional("include_domains"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        "light",
                        "switch",
                        "sensor",
                        "binary_sensor",
                        "cover",
                        "climate",
                        "fan",
                        "lock",
                        "media_player",
                        "vacuum",
                        "water_heater",
                        "camera",
                        "alarm_control_panel",
                        "device_tracker",
                        "remote",
                        "button",
                        "input_boolean",
                        "input_datetime",
                        "input_number",
                        "input_select",
                        "input_text",
                        "scene",
                        "script",
                        "sun",
                        "timer",
                        "weather",
                        "zone",
                    ],
                    multiple=True
                )
            ),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle options flow."""
        return ZoneWorkerOptionsFlow(config_entry)


class ZoneWorkerOptionsFlow(config_entries.OptionsFlow):
    """Handle Zone Worker options."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required("include_area", default=self.config_entry.data.get("include_area")): selector.SelectSelector(
                selector.SelectSelectorConfig(options=[self.config_entry.data.get("include_area")], multiple=False)
            ),
            vol.Optional("include_domains", default=self.config_entry.data.get("include_domains")): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        "light",
                        "switch",
                        "sensor",
                        "binary_sensor",
                        "cover",
                        "climate",
                        "fan",
                        "lock",
                        "media_player",
                        "vacuum",
                        "water_heater",
                        "camera",
                        "alarm_control_panel",
                        "device_tracker",
                        "remote",
                        "button",
                        "input_boolean",
                        "input_datetime",
                        "input_number",
                        "input_select",
                        "input_text",
                        "scene",
                        "script",
                        "sun",
                        "timer",
                        "weather",
                        "zone",
                    ],
                    multiple=True
                )
            ),
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
