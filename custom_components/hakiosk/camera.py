import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    name = entry.title
    async_add_entities([HAKioskScreenshotCamera(host, port, name)])

class HAKioskScreenshotCamera(Camera):
    def __init__(self, host, port, name):
        super().__init__()
        self._host = host
        self._port = port
        self._attr_name = f"{name} Ecrã"
        self._attr_unique_id = f"hakiosk_cam_{host}_{port}"

    async def async_camera_image(self, width=None, height=None):
        async with aiohttp.ClientSession() as session:
            try:
                # Our app has /screenshot endpoint
                async with session.get(f"http://{self._host}:{self._port}/screenshot", timeout=5) as response:
                    if response.status == 200:
                        return await response.read()
            except Exception:
                pass
        return None
