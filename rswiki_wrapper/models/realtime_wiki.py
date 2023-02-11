from __future__ import annotations

import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import BaseResponse

# from rswiki_wrapper import enums


__all__ = ("RealtimePriceResponse",)


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
