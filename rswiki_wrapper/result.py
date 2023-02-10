"""The result type and its variants."""

from __future__ import annotations

import abc
import typing as t

from rswiki_wrapper import errors

__all__ = ("Err", "Ok", "Result")

T = t.TypeVar("T")
E = t.TypeVar("E")


class Result(t.Generic[T, E]):
    """Represents a potential `Ok` or `Err` result.

    This class cannot be instantiated, only its children can be.
    """

    def __new__(cls, *_args: t.Any, **_kwargs: t.Any) -> Result[T, E]:
        if cls is Result:
            raise TypeError("Only Result subclasses can be instantiated.")

        return object.__new__(cls)

    def __init__(self, value: T | None, error: E | None) -> None:
        self._value = value
        self._error = error

    def __repr__(self) -> str:
        inner = self._value if self.is_ok else self._error
        return f"{self.__class__.__name__}({inner})"

    @property
    @abc.abstractmethod
    def is_ok(self) -> bool:
        """`True` if this result is the `Ok` variant."""

    @property
    @abc.abstractmethod
    def is_err(self) -> bool:
        """`True` if this result is the `Err` variant."""

    @abc.abstractmethod
    def unwrap(self) -> T:
        """Unwraps the result to produce the value.

        Returns:
            `T`: The unwrapped value.

        Raises:
            `errors.UnwrapError`: If the result was an `Err`, and not `Ok`.
        """

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """Unwraps the result to produce the error.

        Returns:
            `E`: The unwrapped error.

        Raises:
            `errors.UnwrapError`: If the result was an `Ok`, and not an `Err`.
        """


@t.final
class Ok(Result[T, E]):
    """The `Ok` variant of a `Result`."""

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
    """The `Err` variant of a `Result`."""

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
