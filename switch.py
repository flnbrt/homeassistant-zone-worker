from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from typing import List
import logging

# Define the logger instance
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Zone Worker switches from a config entry."""
    _LOGGER.info("Setting up Zone Worker entry: %s", config_entry.data)

    room_name = config_entry.data["room_name"]
    domains = config_entry.data["domains"].split(",")
    include_entities = config_entry.data["include_entities"].split(",") if config_entry.data["include_entities"] else []
    exclude_entities = config_entry.data["exclude_entities"].split(",") if config_entry.data["exclude_entities"] else []

    _LOGGER.debug(f"Entities to include: {include_entities}")
    _LOGGER.debug(f"Entities to exclude: {exclude_entities}")

    async_add_entities(
        [
            ZoneWorkerSwitch(
                hass,
                f"Zone Worker {room_name}",
                room_name,
                domains,
                include_entities,
                exclude_entities,
            )
        ]
    )

    _LOGGER.debug("Entities added to async_add_entities.")

class ZoneWorkerSwitch(SwitchEntity):
    """Representation of a Zone Worker switch."""

    def __init__(self, hass, name, room_name, domains, include_entities, exclude_entities):
        """Initialize the switch."""
        self.hass = hass
        self._name = name
        self._room_name = room_name
        self._domains = domains
        self._include_entities = include_entities
        self._exclude_entities = exclude_entities
        self._entities = self._gather_entities()
        self._is_on = False

        # Set a unique entity ID (e.g., zone_worker_wohnzimmer)
        self.entity_id = f"switch.zone_worker_{room_name.lower().replace(' ', '_')}"

    def _gather_entities(self):
        """Gather all relevant entities based on room, domains, includes, and excludes."""
        entities = []

        # Iteriere durch alle States und prüfe, ob sie in den angegebenen Raum und Domänen passen
        for state in self.hass.states.async_all():
            entity_id = state.entity_id
            domain = entity_id.split(".")[0]  # Extrahiere die Domäne

            # Füge Entitäten hinzu, die im Raum sind und zu einer der angegebenen Domänen gehören
            if (
                (not self._room_name or self._room_name in state.attributes.get("area_id", ""))
                and (domain in self._domains)  # Füge die Entität hinzu, wenn ihre Domäne angegeben ist
                and (not self._exclude_entities or entity_id not in self._exclude_entities)  # Ausschließen nach Bedarf
            ):
                entities.append(entity_id)

        # Explizite Einschlüsse vornehmen, auch wenn sie nicht zu den oben genannten Kriterien passen
        if self._include_entities:
            for entity in self._include_entities:
                if entity not in entities:
                    entities.append(entity)

        return entities

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.debug(f"Turning on switch: {self._name}")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.debug(f"Turning off switch: {self._name}")
        self._is_on = False
        self.async_write_ha_state()

    async def async_update(self):
        """Fetch new state data for the switch."""
        _LOGGER.debug(f"Updating state for {self._name}")
        self._is_on = any(
            self.hass.states.get(entity) is not None and self.hass.states.get(entity).state == "on"
            for entity in self._entities
        )
        _LOGGER.debug(f"Switch state for {self._name}: {self._is_on}")
