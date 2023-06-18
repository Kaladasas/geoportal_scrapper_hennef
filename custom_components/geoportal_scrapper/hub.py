from __future__ import annotations
from datetime import timedelta
import json
import requests
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVALL = timedelta(seconds=30)

class Hub:

    def __init__(self, hass: HomeAssistant, url_list: list) -> None:
        """Init hub"""
        self.connectors = []
        _LOGGER.debug("# Init hub")
        
        for url in url_list:
            connector = GeoportalConnector(hass, url)
            self.connectors.append(connector)


class GeoportalConnector(DataUpdateCoordinator):
    """One connector per url"""

    def __init__(self, hass: HomeAssistant, url: str) -> None:
        """Init geoportal connector"""
        
        self.category = url.replace("https://geoportal.stadt-hennef.de/mapserver/rest/services/Hosted/",
        "").split("_")[0]
        
        _LOGGER.debug(f"#Create connector for {self.category}")
        
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=f"{DOMAIN}-{self.category}-coordinator",
            update_interval=UPDATE_INTERVALL,
        )
        
        self.hass = hass
        self.url = url
    
    
    async def async_setup(self):
        """Setup connector and fill device data"""
        self.devices = await self.collect_data()
    
    
    async def _async_update_data(self) -> None:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        self.devices = await self.collect_data()
        
        
    async def collect_data(self):
        _LOGGER.debug(f"# Collect data for connector {self.category}")
        device_dict = {}
        
        response = await self.hass.async_add_executor_job(requests.get, self.url)
        data = json.loads(response.content.decode('utf-8'))
        
        for feature in data["features"]:
            globalid = feature["attributes"]["globalid"]
            device_dict[globalid] = {}
            name = feature["attributes"]["name"]
            attributes = feature.get("attributes")
            filtered_attributes = {}
            for key, value in attributes.items():
                if key != "globalid":
                    device_dict[globalid][key] = value
                    
        return device_dict
