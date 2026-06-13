import logging
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER, Platform.CAMERA, Platform.SWITCH, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]

    # Register Services
    async def handle_speak(call):
        message = call.data.get("message")
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{host}:{port}/notify?title=HAKiosk&message={message}")

    async def handle_navigate(call):
        url = call.data.get("url")
        # Note: We need a navigate endpoint in the app, or use existing remote command logic
        # For now, let's assume /navigate?url= exists or use the remote system
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{host}:{port}/navigate?url={url}")

    async def handle_dashlet(call):
        dash_id = call.data.get("id")
        label = call.data.get("label")
        value = call.data.get("value")
        unit = call.data.get("unit", "")
        icon = call.data.get("icon", "")

        async with aiohttp.ClientSession() as session:
            url = f"http://{host}:{port}/dashlet?id={dash_id}&label={label}&value={value}&unit={unit}&icon={icon}"
            await session.get(url)

    hass.services.async_register(DOMAIN, "speak", handle_speak)
    hass.services.async_register(DOMAIN, "navigate", handle_navigate)
    hass.services.async_register(DOMAIN, "update_dashlet", handle_dashlet)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
