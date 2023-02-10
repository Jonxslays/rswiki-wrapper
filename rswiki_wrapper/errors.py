"""Errors that can be raised by the library."""

from rswiki_wrapper import routes

__all__ = (
    "ConflictingArgumentError",
    "HttpError",
    "MissingArgumentError",
    "RsWikiError",
    "UnwrapError",
)


class RsWikiError(Exception):
    """The base error all rswiki error inherit from."""


class HttpError(RsWikiError):
    """Taised when an HTTP request retuns a non 2XX status code."""

    def __init__(self, route: routes.CompiledRoute, message: str) -> None:
        super().__init__(f"HTTP exception in {route.pretty()}: {message}")


class UnwrapError(RsWikiError):
    """Raised when calling `unwrap` or `unwrap_err` incorrectly."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Unwrap failed: {message}")


class MissingArgumentError(RsWikiError):
    """Raised when required arguments were missing."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Missing required argument: {message}")


class ConflictingArgumentError(RsWikiError):
    """Raised when one or more arguments conflict with each other."""

    def __init__(self, *args: str) -> None:
        super().__init__(f"Arguments conflict: {', '.join(args)}")
