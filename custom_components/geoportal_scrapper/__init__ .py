"""
Custom integration to create devices from JSON data.
"""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

from . import hub

url_list = ["https://geoportal.stadt-hennef.de/mapserver/rest/services/Hosted/Solaranlagen_Ansicht/FeatureServer/0/query?where=1%3D1&outFields=*&f=json",
            "https://geoportal.stadt-hennef.de/mapserver/rest/services/Hosted/Breeze_Sensoren_Ansicht/FeatureServer/2/query?where=1%3D1&outFields=*&f=json",
            "https://geoportal.stadt-hennef.de/mapserver/rest/services/Hosted/Parkhaus_Ansicht/FeatureServer/0/query?where=1%3D1&outFields=*&f=json",
            "https://geoportal.stadt-hennef.de/mapserver/rest/services/Hosted/Pegelstand_Ansicht/FeatureServer/2/query?where=1%3D1&outFields=*&f=json"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Mandatory setup function to initilize this component
    """
    _LOGGER.debug(f"# Start loading geoportal scrapper {entry.entry_id}")
    hass.data.setdefault(DOMAIN, {})
    geoportal_hub = hub.Hub(hass, url_list)
    hass.data[DOMAIN][entry.entry_id] = geoportal_hub
    
    for coordinator in geoportal_hub.connectors:
        # Scrap the attributes and values for the first time
        await coordinator.async_setup()

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_forward_entry_setups` function in each platform module.
    _LOGGER.debug("# Forward to sensor")
    await hass.config_entries.async_forward_entry_setup(entry, Platform.SENSOR)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry
    This is called when an entry/configured device is to be removed. The class
    needs to unload itself, and remove callbacks. See the classes for further details
    """
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
