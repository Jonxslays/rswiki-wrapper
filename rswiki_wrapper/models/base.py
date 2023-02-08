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

    def _from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _from_iso_maybe(self, timestamp: str | None) -> datetime | None:
        return self._from_iso(timestamp) if timestamp else None
