"""Switch platform for Zone Worker."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up Zone Worker switches from a config entry."""
    config = hass.data[DOMAIN][entry.entry_id]

    room_name = config["room_name"]
    domains = config["domains"]
    include_entities = config.get("include_entities", [])
    exclude_entities = config.get("exclude_entities", [])

    switches = []
    # Create the main Zone Worker switch
    switches.append(
        ZoneWorkerSwitch(hass, f"Zone Worker {room_name}", room_name, domains, include_entities, exclude_entities)
    )

    # Create domain-specific switches
    for domain in domains:
        switches.append(
            ZoneWorkerSwitch(
                hass, f"Zone Worker {room_name} {domain}", room_name, [domain], include_entities, exclude_entities
            )
        )

    async_add_entities(switches)


class ZoneWorkerSwitch(SwitchEntity):
    """Representation of a Zone Worker switch."""

    def __init__(self, hass, name, room_name, domains, include_entities, exclude_entities):
        self.hass = hass
        self._name = name
        self._room_name = room_name
        self._domains = domains
        self._include_entities = include_entities
        self._exclude_entities = exclude_entities
        self._state = False
        self._entities = self._gather_entities()

    def _gather_entities(self):
        """Gather all entities that match the configuration."""
        entities = []
        for entity_id, state in self.hass.states.async_all().items():
            domain = entity_id.split(".")[0]
            if domain in self._domains or entity_id in self._include_entities:
                if entity_id not in self._exclude_entities:
                    entities.append(entity_id)
        return entities

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_update(self):
        """Update the switch state based on the entities."""
        self._state = any(self.hass.states.get(entity).state == "on" for entity in self._entities)
