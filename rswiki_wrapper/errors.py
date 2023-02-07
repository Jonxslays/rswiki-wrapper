from rswiki_wrapper import routes


class HttpError(Exception):
    def __init__(self, route: routes.CompiledRoute, message: str) -> None:
        super().__init__(f"HTTP exception in {route.pretty()}: {message}")
