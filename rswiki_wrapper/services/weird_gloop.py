from __future__ import annotations

import typing as t

from rswiki_wrapper import contracts
from rswiki_wrapper import enums
from rswiki_wrapper import errors
from rswiki_wrapper import models
from rswiki_wrapper import result
from rswiki_wrapper import routes

__all__ = ("WeirdGloopService",)


@t.final
class WeirdGloopService(contracts.WeirdGloopContract):
    __slots__ = ("_http",)

    def __init__(self, http_service: contracts.HttpContract) -> None:
        self._http = http_service

    async def _fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        return await self._http.fetch(route)

    async def get_vos(self) -> models.VosResponse:
        route = routes.VOS.compile()
        data = await self._fetch(route)
        return models.VosResponse.from_raw(data)

    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        route = routes.VOS_HISTORY.compile().with_params({"page": page})
        data = await self._fetch(route)
        return models.VosHistoryResponse.from_raw(data)

    async def get_latest_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        route = routes.LATEST_EXCHANGE_UPDATE.compile()
        data = await self._fetch(route)
        return models.LatestExchangeUpdateResponse.from_raw(data)

    async def get_social_feed(self, page: int) -> models.SocialFeedResponse:
        route = routes.SOCIAL_FEED.compile().with_params({"page": page})
        data = await self._fetch(route)
        return models.SocialFeedResponse.from_raw(data)

    async def get_latest_price(
        self, game: enums.GameType, *ids_or_names: str | int
    ) -> result.Result[list[models.LatestPriceResponse], models.ErrorResponse]:
        if not ids_or_names:
            raise errors.MissingArgumentError("You must specify at least 1 id or name.")

        params: dict[str, str | int] = {}
        # Weird gloop allows searching multiple items with pipes
        if ids := "|".join(str(i) for i in ids_or_names if isinstance(i, int)):
            params["id"] = ids

        if names := "|".join(n for n in ids_or_names if isinstance(n, str)):
            params["name"] = names

        route = routes.LATEST_PRICE.compile(game.value).with_params(params)
        data = await self._fetch(route)

        if "error" in data:
            return result.Result[list[models.LatestPriceResponse], models.ErrorResponse](
                None, models.ErrorResponse.from_raw(data)
            )

        prices: list[models.LatestPriceResponse] = []
        for key, value in data.items():
            response = models.LatestPriceResponse.from_raw(value)
            response.identifier = key
            prices.append(response)

        return result.Result[list[models.LatestPriceResponse], models.ErrorResponse](prices, None)
