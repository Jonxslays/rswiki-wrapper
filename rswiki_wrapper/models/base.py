from __future__ import annotations

import abc
import typing as t
from dataclasses import dataclass


@dataclass(slots=True, init=False)
class BaseResponse(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_raw(cls, data: dict[str, t.Any]) -> BaseResponse:
        """Deserializes json data into a new instance of this class."""
