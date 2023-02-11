from __future__ import annotations

import typing as t
from datetime import datetime

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

    async def _set_price_params_and_fetch(
        self,
        game: enums.WgGameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
        params: dict[str, str | int],
    ) -> dict[str, t.Any]:
        if not id and not name:
            raise errors.MissingArgumentError("You must specify at least 1 id or name.")

        if id:
            params["id"] = id

        if name:
            params["name"] = name

        if locale:
            params["lang"] = locale.value

        route = routes.HISTORICAL_EXCHANGE_PRICE.compile(
            game.value, time_filter.value
        ).with_params(params)
        return await self._fetch(route)

    async def _set_tms_name_params_and_fetch(
        self,
        names: tuple[str],
        locale: enums.Locale | None,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
        params: dict[str, str | int],
    ) -> dict[str, t.Any]:
        if not names:
            raise errors.MissingArgumentError("please provide one or more names.")

        params["name"] = "|".join(names)
        if locale:
            params["lang"] = locale.value

        self._set_generic_tms_params(start_at, end_at, count, params)
        route = routes.TMS_SEARCH.compile().with_params(params)
        return await self._fetch(route)

    async def _set_tms_id_params_and_fetch(
        self,
        ids: tuple[int],
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
        params: dict[str, str | int],
    ) -> dict[str, t.Any]:
        if not ids:
            raise errors.MissingArgumentError("please provide one or more ids.")

        params["id"] = "|".join(str(i) for i in ids)
        if not params.get("lang"):
            # We're alrady doing a full search
            params["lang"] = "id"

        self._set_generic_tms_params(start_at, end_at, count, params)
        route = routes.TMS_SEARCH.compile().with_params(params)
        return await self._fetch(route)

    def _set_generic_tms_params(
        self,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
        params: dict[str, str | int],
    ) -> None:
        if count is not None and end_at is not None:
            raise errors.ConflictingArgumentError("count", "end_at")

        if start_at:
            params["start"] = start_at.isoformat()

        if end_at:
            params["end"] = end_at.isoformat()

        if count:
            params["number"] = count

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

    async def get_social_feed(self, page: int) -> models.PaginatedSocialFeedResponse:
        route = routes.SOCIAL_FEED.compile().with_params({"page": page})
        data = await self._fetch(route)
        return models.PaginatedSocialFeedResponse.from_raw(data)

    async def get_latest_social_feed(self) -> models.SocialFeedResponse:
        route = routes.LATEST_SOCIAL_FEED.compile()
        data = await self._fetch(route)
        return models.SocialFeedResponse.from_raw(data)

    async def get_latest_exchange_price(
        self, game: enums.WgGameType, *ids_or_names: str | int, locale: enums.Locale | None
    ) -> result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]:
        if not ids_or_names:
            raise errors.MissingArgumentError("You must specify at least 1 id or name.")

        params: dict[str, str | int] = {}
        # Weird gloop allows searching multiple items with pipes
        if ids := "|".join(str(i) for i in ids_or_names if isinstance(i, int)):
            params["id"] = ids

        # Currently only id is taken into account if both id and name are sent together
        # Still sending both in case that behavior ever changes and you can use both
        if names := "|".join(n for n in ids_or_names if isinstance(n, str)):
            params["name"] = names

        if locale:
            params["lang"] = locale.value

        route = routes.LATEST_EXCHANGE_PRICE.compile(game.value).with_params(params)
        data = await self._fetch(route)

        if "error" in data:
            return result.Err[list[models.ExchangePriceResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        prices: list[models.ExchangePriceResponse] = []
        for key, value in data.items():
            response = models.ExchangePriceResponse.from_raw(value)
            response.identifier = key
            prices.append(response)

        return result.Ok[list[models.ExchangePriceResponse], models.ErrorResponse](prices)

    async def get_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]:
        data = await self._set_price_params_and_fetch(
            game, time_filter, id=id, name=name, locale=locale, params={}
        )

        if "error" in data:
            return result.Err[list[models.ExchangePriceResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        prices: list[models.ExchangePriceResponse] = []
        for key, value in data.items():
            for price in value:
                response = models.ExchangePriceResponse.from_raw(price)
                response.identifier = key
                prices.append(response)

        return result.Ok[list[models.ExchangePriceResponse], models.ErrorResponse](prices)

    async def get_compressed_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.CompressedExchangePriceResponse], models.ErrorResponse]:
        data = await self._set_price_params_and_fetch(
            game, time_filter, id=id, name=name, locale=locale, params={"compress": "true"}
        )

        if "error" in data:
            return result.Err[list[models.CompressedExchangePriceResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        prices: list[models.CompressedExchangePriceResponse] = []
        for key, value in data.items():
            prices.extend(
                models.CompressedExchangePriceResponse.from_raw({key: pair}) for pair in value
            )

        return result.Ok[list[models.CompressedExchangePriceResponse], models.ErrorResponse](
            prices
        )

    async def get_current_tms(self) -> list[models.TmsResponse]:
        route = routes.TMS_CURRENT.compile().with_params({"lang": "full"})
        data: list[dict[str, str]] = await self._fetch(route)  # type: ignore
        return [models.TmsResponse.from_raw(item) for item in data]

    async def get_next_tms(self) -> list[models.TmsResponse]:
        route = routes.TMS_NEXT.compile().with_params({"lang": "full"})
        data: list[dict[str, str]] = await self._fetch(route)  # type: ignore
        return [models.TmsResponse.from_raw(item) for item in data]

    async def search_tms_by_name(
        self,
        *names: str,
        locale: enums.Locale | None,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchResponse], models.ErrorResponse]:
        params: dict[str, str | int] = {}
        data = await self._set_tms_name_params_and_fetch(
            names, locale, start_at, end_at, count, params
        )

        if "error" in data:
            return result.Err[list[models.TmsSearchResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        # This endpoint returns a dict on error, or list of dicts on success
        buffer: list[dict[str, str]] = data  # type: ignore
        assert isinstance(buffer, list)

        return result.Ok[list[models.TmsSearchResponse], models.ErrorResponse](
            [models.TmsSearchResponse.from_raw(tms) for tms in buffer]
        )

    async def search_tms_by_id(
        self,
        *ids: int,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchResponse], models.ErrorResponse]:
        params: dict[str, str | int] = {}
        data = await self._set_tms_id_params_and_fetch(ids, start_at, end_at, count, params)

        if "error" in data:
            return result.Err[list[models.TmsSearchResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        # This endpoint returns a dict on error, or list of dicts on success
        buffer: list[dict[str, str]] = data  # type: ignore
        assert isinstance(buffer, list)

        return result.Ok[list[models.TmsSearchResponse], models.ErrorResponse](
            [models.TmsSearchResponse.from_raw(tms) for tms in buffer]
        )

    async def search_tms_by_id_full(
        self,
        *ids: int,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchFullResponse], models.ErrorResponse]:
        params: dict[str, str | int] = {"lang": "full"}
        data = await self._set_tms_id_params_and_fetch(ids, start_at, end_at, count, params)

        if "error" in data:
            return result.Err[list[models.TmsSearchFullResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        # This endpoint returns a dict on error, or list of dicts on success
        buffer: list[dict[str, str]] = data  # type: ignore
        assert isinstance(buffer, list)

        return result.Ok[list[models.TmsSearchFullResponse], models.ErrorResponse](
            [models.TmsSearchFullResponse.from_raw(tms) for tms in buffer]
        )
