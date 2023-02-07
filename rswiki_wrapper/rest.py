from __future__ import annotations

import typing as t

import aiohttp

from rswiki_wrapper import errors
from rswiki_wrapper import routes


class RestClient:
    __slots__ = ("_session",)

    def __init__(self, project_name: str, contact_info: str) -> None:
        self._session = aiohttp.ClientSession(
            headers={"User-Agent": " - ".join((project_name, contact_info))}
        )

    async def fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        url = route.base.value + route.uri

        async with self._session.get(url, params=route.params) as resp:
            if not resp.ok:
                raise errors.HttpError(route, await resp.text())

            return await resp.json()

    async def close(self) -> None:
        await self._session.close()
