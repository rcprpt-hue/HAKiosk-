import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    device_id = entry.data.get("device_id", "hakiosk_device")
    name = entry.title

    device_info = DeviceInfo(
        identifiers={(DOMAIN, device_id)},
        name=name,
        manufacturer="iNFOREIS",
        model="HAKiosk Tablet",
        sw_version="3.4",
    )

    async_add_entities([
        HAKioskRestartButton(host, port, name, device_info),
        HAKioskClearCacheButton(host, port, name, device_info)
    ])

class HAKioskRestartButton(ButtonEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_restart"
        self._attr_name = "Reiniciar App"
        self._attr_icon = "mdi:restart"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/restart")

class HAKioskClearCacheButton(ButtonEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_clear_cache"
        self._attr_name = "Limpar Cache"
        self._attr_icon = "mdi:cached"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/clearCache")
