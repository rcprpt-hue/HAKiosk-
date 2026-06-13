import aiohttp
from homeassistant.components.number import NumberEntity
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
        HAKioskVolumeNumber(host, port, name, device_info),
        HAKioskBrightnessNumber(host, port, name, device_info)
    ])

class HAKioskVolumeNumber(NumberEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_volume"
        self._attr_name = "Volume"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    async def async_set_native_value(self, value):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/volume?level={int(value)}")

class HAKioskBrightnessNumber(NumberEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_brightness"
        self._attr_name = "Brilho"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    async def async_set_native_value(self, value):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/brightness?level={int(value)}")
