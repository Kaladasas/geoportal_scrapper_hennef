from __future__ import annotations
from typing import Any

import json
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import DOMAIN
_LOGGER = logging.getLogger(__name__)

# Definition der Funktion, die von Home Assistant aufgerufen wird, um das Gerät zu erstellen
async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry,
                                async_add_entities: AddEntitiesCallback):

    hub = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("# Init sensors")
    
    sensor_list = []
    for connector in hub.connectors:
        for device_id, entity_dict in connector.devices.items():
            device_name = entity_dict["name"]
            for entity_name, entity_state in entity_dict.items():
                if entity_name is not "name":
                    sensor_list.append(GeoportalSensor(connector, entity_name, entity_state, device_id, device_name))
    
    async_add_entities(sensor_list)


# Definition der Klasse fuer das Geraet
class GeoportalSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, state, device_id, device_name):
        _LOGGER.debug(f"# Create sensor {name} for device {device_name}")
        super().__init__(coordinator)
        self._name = name
        self._state = state
        self._device_id = device_id
        self._device_name = device_name

    # Diese Methode gibt die aktuellen Sensorwerte zurueck
    @property
    def native_value(self) -> str | None:
        """Return the value reported by the sensor."""
        return self.coordinator.devices[self._device_id].get(self._name, "")

    # Diese Methode gibt den Namen des Sensors zurück
    @property
    def name(self):
        return self._name
        
    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return f"{self._device_id}_{self._name}"
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information."""
        return DeviceInfo(
            configuration_url= f"{self.coordinator.url}",
            identifiers={(DOMAIN, self._device_id)},
            manufacturer="Klimakleber",
            model="GeoportalDevice",
            name=self._device_name,
        )
