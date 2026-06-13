import aiohttp
from homeassistant.components.camera import Camera
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

    async_add_entities([HAKioskScreenshotCamera(host, port, name, device_info)])

class HAKioskScreenshotCamera(Camera):
    def __init__(self, host, port, name, device_info):
        super().__init__()
        self._host = host
        self._port = port
        self._attr_device_info = device_info
        self._attr_unique_id = f"{list(device_info['identifiers'])[0][1]}_screenshot"
        self._attr_name = "Ecrã"

    async def async_camera_image(self, width=None, height=None):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{self._host}:{self._port}/screenshot", timeout=5) as response:
                    if response.status == 200:
                        return await response.read()
            except Exception:
                pass
        return None
