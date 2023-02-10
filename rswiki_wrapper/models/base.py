from __future__ import annotations

import abc
import typing as t
from dataclasses import dataclass
from datetime import datetime

__all__ = ("BaseResponse",)


PT_MONTH_MAPPING = {
    "janeiro": "January",
    "fevereiro": "February",
    "marchar": "March",
    "abril": "April",
    "maio": "May",
    "junho": "June",
    "julho": "July",
    "agosto": "August",
    "setembro": "Semptember",
    "outubro": "October",
    "novembro": "November",
    "dezembro": "December",
}


@dataclass(slots=True, init=False)
class BaseResponse(abc.ABC):
    """All response models inherit from this clas.."""

    @classmethod
    @abc.abstractmethod
    def from_raw(cls, data: dict[str, t.Any]) -> BaseResponse:
        """Deserializes json data into a new instance of this class."""

    def _dt_from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _dt_from_iso_maybe(self, timestamp: str | None) -> datetime | None:
        return self._dt_from_iso(timestamp) if timestamp else None

    def _dt_from_epoch(self, timestamp: int, millis: bool = False) -> datetime:
        return datetime.fromtimestamp(timestamp / 1e3 if millis else timestamp)

    def _dt_from_strp(self, date: str) -> datetime:
        return datetime.strptime(date, "%d %B %Y")

    def _dt_from_pt(self, date: str) -> datetime:
        day, month, year = date.split(" de ")
        month = PT_MONTH_MAPPING[month.lower()]
        return self._dt_from_strp(f"{day} {month} {year}")
