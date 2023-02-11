from __future__ import annotations

import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import BaseResponse

# from rswiki_wrapper import enums


__all__ = (
    "AveragePriceResponse",
    "MappingResponse",
    "RealtimePriceResponse",
    "TimeSeriesPriceResponse",
    "TimeFilteredPriceResponse",
)


@dataclass(slots=True, init=False)
class RealtimePriceResponse(BaseResponse):
    """Realtime price of an item based on Runelite price data."""

    id: int
    """The item id associated with this price."""
    high: int | None
    """The current high price or `None` if no high price was found."""
    high_time: datetime | None
    """The timestamp for the high price or `None` if no high price time was found."""
    low: int | None
    """The current low price or `None` if no low price was found."""
    low_time: datetime | None
    """The timestamp for the low price or `None` if no low price time was found."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> RealtimePriceResponse:
        self = cls()

        high_time = data["highTime"]
        low_time = data["lowTime"]

        self.high = data["high"]
        self.low = data["low"]
        self.high_time = self._dt_from_epoch(high_time) if high_time else high_time
        self.low_time = self._dt_from_epoch(low_time) if low_time else low_time

        return self


@dataclass(slots=True, init=False)
class MappingResponse(BaseResponse):
    """Mapping data returned from the realtime API for an item.."""

    id: int
    """The item's id."""
    name: str
    """The item name"""
    examine: str
    """The exmine text of the item."""
    members: bool
    """Whether or not this is a members item."""
    low_alch: int | None
    """The low alch value of the item, or `None` if not alchable."""
    high_alch: int | None
    """The high alch value of the item, or `None` if not alchabl."""
    value: int
    """The grand exchange value of the item."""
    icon: str
    """The icon image filename on the realtime API."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> MappingResponse:
        self = cls()
        self.high_alch = data.get("highalch")
        self.low_alch = data.get("lowalch")

        for attr in self.__dataclass_fields__:
            if attr not in ("high_alch", "low_alch"):
                setattr(self, attr, data[attr])

        return self


@dataclass(slots=True, init=False)
class AveragePriceResponse(BaseResponse):
    """An average price over some amount of time."""

    id: int
    """The item's id."""
    high: int
    """The average high price."""
    low: int
    """The average low price."""
    high_volume: int
    """The volume traded at the high price."""
    low_volume: int
    """The volume traded at the low price."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> AveragePriceResponse:
        self = cls()
        self.high = data["avgHighPrice"]
        self.low = data["avgLowPrice"]
        self.high_volume = data["highPriceVolume"]
        self.low_volume = data["lowPriceVolume"]
        return self


@dataclass(slots=True, init=False)
class TimeFilteredPriceResponse(BaseResponse):
    """A list of averages prices for the given timestamp/time period."""

    timestamp: datetime
    """The timestamp of the data."""
    data: list[AveragePriceResponse]
    """The average prices over the provided time period."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> TimeFilteredPriceResponse:
        self = cls()

        self.timestamp = self._dt_from_epoch(data["timestamp"])
        self.data = []

        for item_id, item in data["data"].items():
            price = AveragePriceResponse.from_raw(item)
            price.id = int(item_id)
            self.data.append(price)

        return self


@dataclass(slots=True, init=False)
class TimeSeriesPriceResponse(AveragePriceResponse):
    """The average price of the item over the given time series."""

    id: int
    """The item's id."""
    high: int
    """The average high price."""
    low: int
    """The average low price."""
    high_volume: int
    """The volume traded at the high price."""
    low_volume: int
    """The volume traded at the low price."""
    timestamp: datetime
    """The timestamp of the data."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> TimeSeriesPriceResponse:
        self = cls()
        self.timestamp = self._dt_from_epoch(data["timestamp"])
        price = AveragePriceResponse.from_raw(data)

        for attr in self.__dataclass_fields__:
            if attr not in ("timestamp", "id"):
                setattr(self, attr, getattr(price, attr))

        return self
