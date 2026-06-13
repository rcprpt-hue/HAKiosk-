import aiohttp
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import CONF_HOST, CONF_PORT, PERCENTAGE
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title

    async_add_entities([
        HAKioskBatterySensor(host, port, name),
        HAKioskMemorySensor(host, port, name)
    ])

class HAKioskBatterySensor(SensorEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Bateria"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/status") as response:
                    data = await response.json()
                    self._attr_native_value = data.get("batteryLevel")
            except:
                self._attr_native_value = None

class HAKioskMemorySensor(SensorEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._attr_name = f"{name} Memória Livre"
        self._attr_native_unit_of_measurement = "MB"

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/status") as response:
                    data = await response.json()
                    self._attr_native_value = data.get("memoryFreeMb")
            except:
                self._attr_native_value = None
