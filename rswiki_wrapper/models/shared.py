from __future__ import annotations

import typing as t
from dataclasses import dataclass

from .base import BaseResponse

__all__ = ("ErrorResponse",)


@dataclass(slots=True, init=False)
class ErrorResponse(BaseResponse):
    """An error returned by the one of the API's."""

    error: str
    """The error message."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> ErrorResponse:
        self = cls()
        self.error = data["error"]
        return self

    @classmethod
    def from_str(cls, err: str) -> ErrorResponse:
        self = cls()
        self.error = err
        return self
