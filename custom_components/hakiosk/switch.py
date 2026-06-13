import aiohttp
from homeassistant.components.switch import SwitchEntity
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
        HAKioskScreenSwitch(host, port, name, device_info),
        HAKioskLockSwitch(host, port, name, device_info),
        HAKioskScreensaverSwitch(host, port, name, device_info)
    ])

class HAKioskScreenSwitch(SwitchEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_screen"
        self._attr_name = "Ecrã"
        self._attr_icon = "mdi:monitor"
        self._attr_is_on = True

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screenOn")
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://{self._host}:{self._port}/screensaver?state=true")
        self._attr_is_on = False

class HAKioskLockSwitch(SwitchEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_lock"
        self._attr_name = "Bloqueio Kiosk"
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
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_screensaver"
        self._attr_name = "Protetor de Ecrã"
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
