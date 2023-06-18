"""Config flow for Hello World integration."""
from __future__ import annotations

import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for geoportal scrapper"""

    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Handle user step."""
        return self.async_create_entry(
            title="geoportal_scrapper",
            data={"test": "test"})


