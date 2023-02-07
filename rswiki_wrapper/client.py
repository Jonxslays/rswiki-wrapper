from __future__ import annotations

import sys
import typing as t

from rswiki_wrapper import constants
from rswiki_wrapper import models
from rswiki_wrapper import rest
from rswiki_wrapper import routes


class Client:
    __slots__ = ("_rest",)

    def __init__(self, project_name: str | None = None, contact_info: str | None = None) -> None:
        warn: t.Callable[[str], None] = lambda attr: print(
            f"{attr} should be set to identify yourself with the API.",
            file=sys.stderr,
        )

        if not project_name:
            warn("Project name")
            project_name = constants.DEFAULT_PROJECT_NAME

        if not contact_info:
            warn("Contact info")
            contact_info = constants.DEFAULT_CONTACT_INFO

        self._rest = rest.RestClient(project_name, contact_info)

    async def close(self) -> None:
        await self._rest.close()

    async def get_vos(self) -> models.VosResponse:
        route = routes.GET_VOS.compile()
        data = await self._rest.fetch(route)
        return models.VosResponse.from_raw(data)

    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        route = routes.GET_VOS_HISTORY.compile().with_params({"page": page})
        data = await self._rest.fetch(route)
        return models.VosHistoryResponse.from_raw(data)

    async def get_last_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        route = routes.LAST_EXCHANGE_UPDATE.compile()
        data = await self._rest.fetch(route)
        return models.LatestExchangeUpdateResponse.from_raw(data)

    async def get_social_feed(self, page: int) -> models.SocialFeedResponse:
        route = routes.GET_SOCIAL_FEED.compile().with_params({"page": page})
        data = await self._rest.fetch(route)
        return models.SocialFeedResponse.from_raw(data)
