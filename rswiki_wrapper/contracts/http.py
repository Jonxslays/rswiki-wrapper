from __future__ import annotations

import abc
import typing as t

from .. import routes

__all__ = ("HttpContract",)


class HttpContract(abc.ABC):
    """The contract required to satisfy the underlying http client.

    Args:
        project_name (`str`): The project name to use in the requst headers.

        contact_info (`str`): The contact info to use in the request headers.
    """

    @abc.abstractmethod
    def __init__(self, project_name: str, contact_info: str) -> None:
        ...

    @abc.abstractmethod
    async def fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        """Makes a get request to the specified route.

        Args:
            route (`routes.CompiledRoute`): The route to request.

        Returns:
            `dict[str, t.Any]`: The resulting json data.
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """Cleans up any resources used by the http implementation."""
