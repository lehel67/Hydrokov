from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfVolume, CONF_EMAIL
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        HydrokovWaterMeter(coordinator, entry),
        HydrokovLatestConsumption(coordinator, entry),
        HydrokovLastReadingDate(coordinator, entry),
        HydrokovLatestInvoice(coordinator, entry),
        HydrokovOutstandingAmount(coordinator, entry),
        HydrokovInvoiceCount(coordinator, entry),
    ]
    async_add_entities(sensors, True)


class HydrokovBase(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"hydrokov_{entry.data[CONF_EMAIL]}_{self.entity_type}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data[CONF_EMAIL])},
            "name": "Hydrokov",
            "manufacturer": "Hydrokov",
        }


# ==================== CONTOR / CONTOARE ====================

class HydrokovWaterMeter(HydrokovBase):
    entity_type = "water_meter"
    _attr_name = "Water Meter Reading"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.VOLUME
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self):
        try:
            indexes = self.coordinator.data.get("index_history", {}).get("indexes", [])
            if indexes:
                return float(indexes[0].get("indexVechi") or indexes[0].get("index") or 0)
        except:
            pass
        return None

    @property
    def extra_state_attributes(self):
        attrs = {}
        try:
            indexes = self.coordinator.data.get("index_history", {}).get("indexes", [])[:8]
            for i, idx in enumerate(indexes, 1):
                attrs[f"reading_{i}"] = f"{idx.get('indexVechi', 'N/A')} m³ → {idx.get('dataCitirii', '')[:10]}"
        except:
            pass
        return attrs


class HydrokovLatestConsumption(HydrokovBase):
    entity_type = "latest_consumption"
    _attr_name = "Latest Consumption"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.VOLUME

    @property
    def native_value(self):
        try:
            indexes = self.coordinator.data.get("index_history", {}).get("indexes", [])
            if len(indexes) >= 2:
                curr = indexes[0].get("indexVechi") or indexes[0].get("index") or 0
                prev = indexes[1].get("indexVechi") or indexes[1].get("index") or 0
                return float(curr) - float(prev)
        except:
            pass
        return 0.0


class HydrokovLastReadingDate(HydrokovBase):
    entity_type = "last_reading_date"
    _attr_name = "Last Reading Date"

    @property
    def native_value(self):
        try:
            indexes = self.coordinator.data.get("index_history", {}).get("indexes", [])
            if indexes:
                return str(indexes[0].get("dataCitirii", ""))[:10]
        except:
            pass
        return None


# ==================== FACTURI ====================

class HydrokovLatestInvoice(HydrokovBase):
    entity_type = "latest_invoice"
    _attr_name = "Latest Invoice"
    _attr_native_unit_of_measurement = "RON"
    _attr_device_class = SensorDeviceClass.MONETARY

    @property
    def native_value(self):
        try:
            invoices = self.coordinator.data.get("invoices", [])
            if invoices:
                return float(invoices[0].get("total_factura") or 0)
        except:
            pass
        return None

    @property
    def extra_state_attributes(self):
        attrs = {"invoices_count": 0}
        try:
            invoices = self.coordinator.data.get("invoices", [])[:6]
            attrs["invoices_count"] = len(invoices)
            for i, inv in enumerate(invoices, 1):
                attrs[f"invoice_{i}"] = (
                    f"{inv.get('numarfactura')} | "
                    f"{inv.get('total_factura')} RON | "
                    f"Due: {str(inv.get('scadenta',''))[:10]}"
                )
        except:
            pass
        return attrs


class HydrokovOutstandingAmount(HydrokovBase):
    entity_type = "outstanding_amount"
    _attr_name = "Outstanding Amount"
    _attr_native_unit_of_measurement = "RON"
    _attr_device_class = SensorDeviceClass.MONETARY

    @property
    def native_value(self):
        try:
            invoices = self.coordinator.data.get("invoices", [])
            if invoices:
                return float(invoices[0].get("rest_plata") or 0)
        except:
            pass
        return None


class HydrokovInvoiceCount(HydrokovBase):
    entity_type = "invoice_count"
    _attr_name = "Total Invoices"

    @property
    def native_value(self):
        try:
            return len(self.coordinator.data.get("invoices", []))
        except:
            return 0