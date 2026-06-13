import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title
    async_add_entities([
        HAKioskScreenSwitch(host, port, name),
        HAKioskLockSwitch(host, port, name),
        HAKioskScreensaverSwitch(host, port, name)
    ])

class HAKioskScreenSwitch(SwitchEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Ecrã"
        self._attr_icon = "mdi:monitor"
        self._attr_is_on = True

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screenOn")
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        # We don't have a direct "off" yet, but we can trigger standby screensaver
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screensaver?state=true")
        self._attr_is_on = False

class HAKioskLockSwitch(SwitchEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Bloqueio Kiosk"
        self._attr_icon = "mdi:lock"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/lock?state=true")
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/lock?state=false")
        self._attr_is_on = False

class HAKioskScreensaverSwitch(SwitchEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Protetor de Ecrã"
        self._attr_icon = "mdi:clock-outline"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screensaver?state=true")
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screensaver?state=false")
        self._attr_is_on = False
