from __future__ import annotations
from typing import Any

import json
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    SensorEntity,
    STATE_CLASS_MEASUREMENT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN
from .sensor_units import get_device_class_and_unit
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry,
                                async_add_entities: AddEntitiesCallback):
    """Mandatory setup function to create sensors and devices"""

    hub = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("# Init sensors")
    
    sensor_list = []
    for connector in hub.connectors:
        for device_id, entity_dict in connector.devices.items():
            device_name = entity_dict["name"]
            for entity_name, entity_state in entity_dict.items():
                if entity_name != "name":
                    device_class, unit = get_device_class_and_unit(connector.category, entity_name)
                    sensor_list.append(GeoportalSensor(connector, entity_name, entity_state, device_id, device_name, device_class, unit))
    
    async_add_entities(sensor_list)


class GeoportalSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor entity"""
    def __init__(self, coordinator, name, state, device_id, device_name, device_class, unit):
        _LOGGER.debug(f"# Create sensor {name} for device {device_name}")
        super().__init__(coordinator)
        self._name = name
        # changing the entity id to make identification easier
        self.entity_id = f"sensor.geoportal_{name}_{device_name.lower()}"
        self._state = state
        self._device_id = device_id
        self._device_name = device_name
        if (unit != None):
            self._attr_state_class = STATE_CLASS_MEASUREMENT
            self._device_class = device_class
            _LOGGER.debug(f"{name}_{device_name.lower()} has unit {unit} and device class {device_class}")
        self._unit = unit

    @property
    def native_value(self) -> str | None:
        """Return the value reported by the sensor"""
        return self.coordinator.devices[self._device_id].get(self._name, "")

    @property
    def name(self):
        """Return the name of the sensor"""
        return self._name
        
    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return f"{self._device_id.lower()}_{self._name.lower()}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement"""
        return self._unit
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information
        
        Needed to assign the sensor to a device
        """
        return DeviceInfo(
            configuration_url= f"{self.coordinator.url}",
            identifiers={(DOMAIN, self._device_id)},
            manufacturer="Klimakleber",
            model=self.coordinator.category,
            name=self._device_name,
        )
