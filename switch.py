"""Zone Worker switch definitions."""
import logging
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.const import STATE_ON
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the switch platform."""

    async def async_setup():
        include_area = config_entry.data['include_area']
        include_domains = config_entry.data.get('include_domains', [])

        # Initialize entity registry
        entity_registry = async_get_entity_registry(hass)

        # Get all entities in the specified area
        area_entities = [
            entity.entity_id for entity in entity_registry.entities.values()
            if entity.area_id == include_area
        ]

        _LOGGER.debug(f"Entities in area {include_area}: {area_entities}")

        # Filter entities by the specified domains (if any)
        if include_domains:
            area_entities = [
                entity for entity in area_entities
                if any(entity.startswith(domain + ".") for domain in include_domains)
            ]

        _LOGGER.debug(f"Entities in area {include_area} with domains {include_domains}: {area_entities}")

        entities_to_add = []

        # Check for existing entities in the registry
        existing_entities = hass.states.async_entity_ids("switch")

        # Create master switch entity
        master_switch = ZoneWorkerMasterSwitch(hass, include_area, area_entities)
        if master_switch.entity_id not in existing_entities:
            entities_to_add.append(master_switch)
        else:
            _LOGGER.info(f"Switch {master_switch.entity_id} already exists, skipping creation.")

        # Create individual switch entities for each domain
        for domain in include_domains:
            domain_entities = [
                entity for entity in area_entities
                if entity.startswith(domain + ".")
            ]
            domain_switch = ZoneWorkerDomainSwitch(hass, include_area, domain, domain_entities)
            if domain_switch.entity_id not in existing_entities:
                entities_to_add.append(domain_switch)
            else:
                _LOGGER.info(f"Switch {domain_switch.entity_id} already exists, skipping creation.")

        if not entities_to_add:
            _LOGGER.warning("No new entities found for the specified area and domains")

        async_add_entities(entities_to_add)

    hass.async_create_task(async_setup())

class ZoneWorkerSwitch(ToggleEntity):
    """Representation of a Zone Worker switch."""

    def __init__(self, hass, name, entities):
        self.hass = hass
        self._name = name
        self._state = False
        self._entities = entities
        self._attr_unique_id = f"zone_worker_{name}"

        _LOGGER.debug(f"Switch '{self._name}' will monitor entities: {self._entities}")

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = False
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Call when entity about to be added to hass."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, self._entities, self._async_entity_state_listener
            )
        )
        self._update_state()

    @callback
    def _async_entity_state_listener(self, event):
        """Handle the state changes of the tracked entities."""
        _LOGGER.debug("Entity %s changed state to %s", event.data['entity_id'], event.data['new_state'].state)
        self._update_state()

    @callback
    def _update_state(self):
        """Update the switch state based on the states of the tracked entities."""
        new_state = any(
            self.hass.states.get(entity_id).state == STATE_ON for entity_id in self._entities
        )
        if new_state != self._state:
            _LOGGER.debug(f"Switch '{self._name}' state changing from {self._state} to {new_state}")
            self._state = new_state
            self.async_write_ha_state()

class ZoneWorkerMasterSwitch(ZoneWorkerSwitch):
    """Representation of a Zone Worker master switch."""

    def __init__(self, hass, area, entities):
        super().__init__(hass, f"switch.area_{area}_master", entities)

class ZoneWorkerDomainSwitch(ZoneWorkerSwitch):
    """Representation of a Zone Worker domain switch."""

    def __init__(self, hass, area, domain, entities):
        super().__init__(hass, f"switch.area_{area}_{domain}", entities)
