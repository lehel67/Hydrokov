import aiohttp
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    coordinator = HydrokovCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


class HydrokovCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.email = entry.data[CONF_EMAIL]
        self.password = entry.data[CONF_PASSWORD]
        self.client_id = entry.data.get("client_id", "TSY4647")
        self.token = None

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL)
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

                # Date contor
                async with session.get(f"https://app.hydrokov.ro/api/index/history/{self.client_id}", headers=headers) as resp:
                    if resp.status == 200:
                        data["index_history"] = await resp.json()

                # Facturi
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