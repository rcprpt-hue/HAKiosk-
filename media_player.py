import aiohttp
import logging
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaType,
)
from homeassistant.const import CONF_HOST, CONF_PORT, STATE_IDLE, STATE_PLAYING
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    async_add_entities([HAKioskMediaPlayer(host, port, entry.title)], True)

class HAKioskMediaPlayer(MediaPlayerEntity):
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = f"{name} Media Player"
        self._state = STATE_IDLE
        self._volume = 0.5

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def volume_level(self):
        return self._volume

    @property
    def supported_features(self):
        return (
            MediaPlayerEntityFeature.PLAY_MEDIA
            | MediaPlayerEntityFeature.STOP
            | MediaPlayerEntityFeature.VOLUME_SET
            | MediaPlayerEntityFeature.VOLUME_STEP
        )

    async def async_update(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{self._host}:{self._port}/status") as response:
                    if response.status == 200:
                        data = await response.json()
                        self._volume = data.get("volume", 50) / 100.0
                        # HAKiosk simple status doesn't track playing state well yet, defaulting to IDLE
                        self._state = STATE_IDLE
        except Exception:
            self._state = STATE_IDLE

    async def async_play_media(self, media_type, media_id, **kwargs):
        async with aiohttp.ClientSession() as session:
            if media_type == MediaType.MUSIC or media_type == "audio/mp3":
                async with session.get(f"http://{self._host}:{self._port}/play", params={"url": media_id}) as response:
                    await response.read()
            else:
                async with session.get(f"http://{self._host}:{self._port}/speak", params={"message": media_id}) as response:
                    await response.read()
        self._state = STATE_PLAYING

    async def async_media_stop(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self._host}:{self._port}/stop") as response:
                await response.read()
        self._state = STATE_IDLE

    async def async_set_volume_level(self, volume):
        level = int(volume * 100)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self._host}:{self._port}/volume", params={"level": level}) as response:
                await response.read()
        self._volume = volume

    async def async_volume_up(self):
        await self.async_set_volume_level(min(1.0, self._volume + 0.1))

    async def async_volume_down(self):
        await self.async_set_volume_level(max(0.0, self._volume - 0.1))
