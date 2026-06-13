import aiohttp
from homeassistant.components.number import NumberEntity
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title
    async_add_entities([
        HAKioskVolumeNumber(host, port, name),
        HAKioskBrightnessNumber(host, port, name)
    ])

class HAKioskVolumeNumber(NumberEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Volume"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    async def async_set_native_value(self, value):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/volume?level={int(value)}")

class HAKioskBrightnessNumber(NumberEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Brilho"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    async def async_set_native_value(self, value):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/brightness?level={int(value)}")
