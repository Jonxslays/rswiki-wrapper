from . import routes

__all__ = ("HttpError", "MissingArgumentError", "RsWikiError", "UnwrapError")


class RsWikiError(Exception):
    ...


class HttpError(RsWikiError):
    def __init__(self, route: routes.CompiledRoute, message: str) -> None:
        super().__init__(f"HTTP exception in {route.pretty()}: {message}")


class UnwrapError(RsWikiError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Unwrap failed: {message}")


class MissingArgumentError(RsWikiError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Missing required argument: {message}")
