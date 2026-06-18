import logging
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER, Platform.CAMERA, Platform.SWITCH, Platform.BUTTON, Platform.MEDIA_PLAYER]

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
            async with session.get(f"http://{host}:{port}/speak", params={"message": message}) as response:
                await response.read()

    async def handle_notify(call):
        title = call.data.get("title", "HAKiosk")
        message = call.data.get("message")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{host}:{port}/notify", params={"title": title, "message": message}) as response:
                await response.read()

    async def handle_play(call):
        url = call.data.get("url")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{host}:{port}/play", params={"url": url}) as response:
                await response.read()

    async def handle_navigate(call):
        url = call.data.get("url")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{host}:{port}/navigate", params={"to": url}) as response:
                await response.read()

    async def handle_dashlet(call):
        dash_id = call.data.get("id")
        label = call.data.get("label")
        value = call.data.get("value")
        unit = call.data.get("unit", "")
        icon = call.data.get("icon", "")

        params = {"id": dash_id, "label": label, "value": value, "unit": unit, "icon": icon}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{host}:{port}/dashlet", params=params) as response:
                await response.read()

    hass.services.async_register(DOMAIN, "speak", handle_speak)
    hass.services.async_register(DOMAIN, "notify", handle_notify)
    hass.services.async_register(DOMAIN, "play", handle_play)
    hass.services.async_register(DOMAIN, "navigate", handle_navigate)
    hass.services.async_register(DOMAIN, "update_dashlet", handle_dashlet)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
