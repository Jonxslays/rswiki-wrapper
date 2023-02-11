from __future__ import annotations

import typing as t

from datetime import datetime

from rswiki_wrapper import contracts
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result
from rswiki_wrapper import routes

__all__ = ("RealtimeService",)


@t.final
class RealtimeService(contracts.RealtimeContract):
    __slots__ = ("_http",)

    def __init__(self, http_service: contracts.HttpContract) -> None:
        self._http = http_service

    async def _fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        return await self._http.fetch(route)

    async def get_price(
        self, game: enums.RtGameType, id: int | None
    ) -> result.Result[list[models.RealtimePriceResponse], models.ErrorResponse]:
        params: dict[str, str | int] = {}
        if id:
            params["id"] = id

        route = routes.REALTIME_PRICE.compile(game.value).with_params(params)
        data = await self._fetch(route)

        if "error" in data:
            return result.Err[list[models.RealtimePriceResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        buffer: list[models.RealtimePriceResponse] = []
        for item_id, item in data["data"].items():
            price = models.RealtimePriceResponse.from_raw(item)
            price.id = int(item_id)
            buffer.append(price)

        return result.Ok[list[models.RealtimePriceResponse], models.ErrorResponse](buffer)

    async def get_mapping(self, game: enums.RtGameType) -> list[models.MappingResponse]:
        route = routes.REALTIME_MAPPING.compile(game.value)
        data: list[dict[str, t.Any]] = await self._fetch(route)  # type: ignore
        return [models.MappingResponse.from_raw(item) for item in data]

    async def get_avg_price(
        self,
        game: enums.TimeSeriesGameType,
        time_filter: enums.RtTimeFilter,
        *,
        timestamp: datetime | None,
    ) -> result.Result[models.TimeFilteredPriceResponse, models.ErrorResponse]:
        params: dict[str, str | int] = {}
        if timestamp:
            # Endpoint only accepts timestamps divisble by 300
            epoch = int(timestamp.timestamp())
            params["timestamp"] = epoch - (epoch % 300)

        route = routes.REALTIME_AVG_PRICE.compile(game.value, time_filter.value).with_params(
            params
        )

        data = await self._fetch(route)
        if "error" in data:
            return result.Err[models.TimeFilteredPriceResponse, models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        return result.Ok[models.TimeFilteredPriceResponse, models.ErrorResponse](
            models.TimeFilteredPriceResponse.from_raw(data)
        )

    async def get_avg_price_by_id(
        self, id: int, game: enums.TimeSeriesGameType, timestep: enums.TimeSeriesFilter
    ) -> result.Result[list[models.TimeSeriesPriceResponse], models.ErrorResponse]:
        params = {"id": id, "timestep": timestep.value}
        route = routes.REALTIME_TIMESERIES.compile(game.value).with_params(params)
        data = await self._fetch(route)

        if "error" in data:
            return result.Err[list[models.TimeSeriesPriceResponse], models.ErrorResponse](
                models.ErrorResponse.from_raw(data)
            )

        buffer: list[models.TimeSeriesPriceResponse] = []
        for item in data["data"]:
            price = models.TimeSeriesPriceResponse.from_raw(item)
            price.id = id
            buffer.append(price)

        return result.Ok[list[models.TimeSeriesPriceResponse], models.ErrorResponse](buffer)
