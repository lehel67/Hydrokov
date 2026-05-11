import aiohttp
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hydrokov from a config entry."""
    coordinator = HydrokovCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, ["sensor"]):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
        if coordinator:
            await coordinator.async_shutdown()
    return unload_ok


class HydrokovCoordinator(DataUpdateCoordinator):
    """Hydrokov data update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.email = entry.data[CONF_EMAIL]
        self.password = entry.data[CONF_PASSWORD]
        self.client_id = entry.data.get("client_id", "TSY4647")
        self.token = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=6),
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                # Login
                async with session.post(
                    "https://app.hydrokov.ro/api/auth",
                    json={"email": self.email, "password": self.password},
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                ) as resp:
                    self.token = (await resp.text()).strip()

                headers = {"X-Auth-Token": self.token, "User-Agent": "Mozilla/5.0"}

                data = {"index_history": {}, "invoices": []}

                # Vízóra adatok
                async with session.get(f"https://app.hydrokov.ro/api/index/history/{self.client_id}", headers=headers) as resp:
                    if resp.status == 200:
                        data["index_history"] = await resp.json()

                # Számlák
                async with session.get(f"https://app.hydrokov.ro/api/invoice/invoices/{self.client_id}", headers=headers) as resp:
                    if resp.status == 200:
                        raw = await resp.json()
                        if isinstance(raw, list):
                            data["invoices"] = raw
                        elif isinstance(raw, dict):
                            data["invoices"] = raw.get("invoices", []) or raw.get("data", [])

                return data

        except Exception as err:
            _LOGGER.error("Hydrokov hiba: %s", err)
            raise UpdateFailed(f"Hiba: {err}") from err