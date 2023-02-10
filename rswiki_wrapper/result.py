from __future__ import annotations

import abc
import typing as t

from . import errors

__all__ = ("Err", "Ok", "Result")

T = t.TypeVar("T")
E = t.TypeVar("E")


class Result(t.Generic[T, E]):
    def __new__(cls, *_args: t.Any, **_kwargs: t.Any) -> Result[T, E]:
        if cls is Result:
            raise TypeError("Only Result subclasses can be instantiated.")

        return object.__new__(cls)

    def __init__(self, value: T | None, error: E | None) -> None:
        self._value = value
        self._error = error

    @property
    @abc.abstractmethod
    def is_ok(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_err(self) -> bool:
        ...

    @abc.abstractmethod
    def unwrap(self) -> T:
        ...

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        ...


@t.final
class Ok(Result[T, E]):
    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_err(self) -> E:
        raise errors.UnwrapError(f"Called unwrap error on an non error value - {self._value}")


@t.final
class Err(Result[T, E]):
    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise errors.UnwrapError(f"Called unwrap on an error value - {self._error}")

    def unwrap_err(self) -> E:
        return self._error
