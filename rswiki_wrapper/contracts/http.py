from __future__ import annotations

import abc
import typing as t

from rswiki_wrapper import routes

__all__ = ("HttpContract",)


class HttpContract(abc.ABC):
    @abc.abstractmethod
    def __init__(self, project_name: str, contact_info: str) -> None:
        ...

    @abc.abstractmethod
    async def fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        ...
