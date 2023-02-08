from __future__ import annotations

import abc
import typing as t
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, init=False)
class BaseResponse(abc.ABC):
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
