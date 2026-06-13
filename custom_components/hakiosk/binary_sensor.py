import aiohttp
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title
    async_add_entities([HAKioskChargingSensor(host, port, name)])

class HAKioskChargingSensor(BinarySensorEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} a Carregar"
        self._attr_device_class = BinarySensorDeviceClass.POWER

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/status") as response:
                    data = await response.json()
                    self._attr_is_on = data.get("isCharging")
            except:
                self._attr_is_on = None
