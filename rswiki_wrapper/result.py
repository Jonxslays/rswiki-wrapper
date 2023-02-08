from __future__ import annotations

import typing as t

from rswiki_wrapper import errors

T = t.TypeVar("T")
E = t.TypeVar("E")


@t.final
class Result(t.Generic[T, E]):
    def __init__(self, value: T | None, error: E | None) -> None:
        self._value = value
        self._error = error

    def is_ok(self) -> bool:
        return not self._error

    def is_err(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error:
            raise errors.UnwrapError(f"Called unwrap on an error value - {self._error}")

        return t.cast(T, self._value)

    def unwrap_err(self) -> E:
        if not self._error:
            raise errors.UnwrapError(f"Called unwrap error on an non error value - {self._value}")

        return self._error
