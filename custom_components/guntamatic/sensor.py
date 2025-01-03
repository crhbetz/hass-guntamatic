"""Platform for sensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GuntamaticConfigEntry, GuntamaticDataUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GuntamaticConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the guntamatic sensors."""

    _LOGGER.info("Called async_setup_entry in sensor.py")
    coordinator = entry.runtime_data
    sensors: list = []
    for sensor_name in coordinator.data:
        _LOGGER.info(
            "Setting up sensor for value %s from data: %s",
            sensor_name,
            coordinator.data[sensor_name],
        )
        if coordinator.data[sensor_name]["unit"] == "°C":
            sensors.append(GuntamaticTemperatureSensor(coordinator, sensor_name))  # noqa: PERF401
        elif coordinator.data[sensor_name]["unit"] == "%":
            sensors.append(GuntamaticPercentageSensor(coordinator, sensor_name))  # noqa: PERF401
        elif coordinator.data[sensor_name]["unit"] == "h":
            sensors.append(GuntamaticHoursSensor(coordinator, sensor_name))  # noqa: PERF401
        elif coordinator.data[sensor_name]["unit"] == "d":
            sensors.append(GuntamaticDaysSensor(coordinator, sensor_name))  # noqa: PERF401
        else:
            sensors.append(GuntamaticStringSensor(coordinator, sensor_name))  # noqa: PERF401

    async_add_entities(sensors, True)


class GuntamaticSensor(CoordinatorEntity, SensorEntity):
    """Representation of a generic Guntamatic Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator)

        device_name = coordinator.config.name
        self.data_name = name
        self.coordinator = coordinator
        self._attr_name = f"{device_name} {name}"
        self._attr_unique_id = f"{device_name}_{name}"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(self.coordinator.data)

    @property
    def should_poll(self) -> bool:
        """Should poll?.

        -> https://aarongodfrey.dev/home%20automation/use-coordinatorentity-with-the-dataupdatecoordinator/ .
        """
        return False

    @property
    def native_value(self) -> int | None:
        """Return the state of the resources if it has been received yet."""
        if self.data_name in self.coordinator.data:
            return self._parse_value(self.coordinator.data[self.data_name]["value"])
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("coordinator update callback received on %s", self._attr_name)
        self.update()

    def _parse_value(self, value):
        """Needs to be implemented by child."""

        raise ValueError("Child of GuntamaticSensor needs to implement _parse_value!")

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self.data_name in self.coordinator.data:
            value = self._parse_value(self.coordinator.data[self.data_name]["value"])
            self.parameter_value = value
            self.async_write_ha_state()
            _LOGGER.debug("Updating state of %s: %s", self._attr_unique_id, value)
        else:
            _LOGGER.debug("Name %s not in data: %s", self.name, self.coordinator.data)


class GuntamaticTemperatureSensor(GuntamaticSensor):
    """Guntamatic Temperature Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator, name)

        # TemperatureSensor specific attributes
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    def _parse_value(self, value) -> float:
        return float(value)


class GuntamaticPercentageSensor(GuntamaticSensor):
    """Guntamatic Percentage Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator, name)

        # TemperatureSensor specific attributes
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    def _parse_value(self, value) -> float:
        return float(value)


class GuntamaticHoursSensor(GuntamaticSensor):
    """Guntamatic Hours Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator, name)

        # TemperatureSensor specific attributes
        self._attr_native_unit_of_measurement = UnitOfTime.HOURS
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    def _parse_value(self, value) -> float:
        return float(value)


class GuntamaticDaysSensor(GuntamaticSensor):
    """Guntamatic Hours Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator, name)

        # TemperatureSensor specific attributes
        self._attr_native_unit_of_measurement = UnitOfTime.DAYS
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    def _parse_value(self, value) -> float:
        return float(value)


class GuntamaticStringSensor(GuntamaticSensor):
    """Guntamatic Generic String Sensor."""

    def __init__(  # noqa: D107
        self,
        coordinator: GuntamaticDataUpdateCoordinator,
        name: str,
    ) -> None:
        super().__init__(coordinator, name)

        # TemperatureSensor specific attributes
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    def _parse_value(self, value) -> float:
        return str(value)
