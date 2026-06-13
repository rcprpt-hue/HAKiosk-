import aiohttp
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import CONF_HOST, CONF_PORT, PERCENTAGE
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
        HAKioskBatterySensor(host, port, name, device_info),
        HAKioskMemorySensor(host, port, name, device_info)
    ])

class HAKioskBatterySensor(SensorEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_battery"
        self._attr_name = "Bateria"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/status", timeout=5) as response:
                    data = await response.json()
                    self._attr_native_value = data.get("batteryLevel")
            except:
                self._attr_native_value = None

class HAKioskMemorySensor(SensorEntity):
    def __init__(self, host, port, name, device_info):
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_memory"
        self._attr_name = "Memória Livre"
        self._attr_native_unit_of_measurement = "MB"

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/status", timeout=5) as response:
                    data = await response.json()
                    self._attr_native_value = data.get("memoryFreeMb")
            except:
                self._attr_native_value = None
