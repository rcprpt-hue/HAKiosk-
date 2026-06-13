import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title
    async_add_entities([
        HAKioskRestartButton(host, port, name),
        HAKioskClearCacheButton(host, port, name)
    ])

class HAKioskRestartButton(ButtonEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Reiniciar App"
        self._attr_icon = "mdi:restart"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/restart")

class HAKioskClearCacheButton(ButtonEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Limpar Cache"
        self._attr_icon = "mdi:cached"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/clearCache")
