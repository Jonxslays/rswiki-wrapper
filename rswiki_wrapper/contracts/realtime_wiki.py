from __future__ import annotations

import abc
from datetime import datetime

from .http import HttpContract
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result

__all__ = ("RealtimeContract",)


class RealtimeContract(abc.ABC):
    """The contract required to satify the realtime wiki API.

    Args:
        http_service (`contracts.HttpContract`): The http service to use to satify
            this contract.
    """

    @abc.abstractmethod
    def __init__(self, http_service: HttpContract) -> None:
        ...

    @abc.abstractmethod
    async def get_price(
        self, game: enums.RtGameType, id: int | None
    ) -> result.Result[list[models.RealtimePriceResponse], models.ErrorResponse]:
        """Gets the latest realtime price data from Runelite.

        NOTE:
            Consider fetching all prices once, and caching them for a period of time.
            Then just do cache lookups for individual ID's. Reduces stress on the API.


        Args:
            game (`enums.RtGameType`): The game type to get the prices for.

            id (`int | None`): The item id to search for. If `None`, all known items
                are returned.

        Returns:
            `result.Result[list[models.RealtimePriceResponse], models.ErrorResponse]`:
                A result containing the list of prices, or an error.
        """

    @abc.abstractmethod
    async def get_mapping(self, game: enums.RtGameType) -> list[models.MappingResponse]:
        """Gets a mapping of miscellaneous item data from the realtime API.

        Args:
            game (`enums.RtGameType`): The game type to get the mapping for.

        Returns:
            `list[models.MappingResponse]`: A list containing the requested data.
        """

    @abc.abstractmethod
    async def get_avg_price(
        self,
        game: enums.TimeSeriesGameType,
        time_filter: enums.RtTimeFilter,
        *,
        timestamp: datetime | None,
    ) -> result.Result[models.TimeFilteredPriceResponse, models.ErrorResponse]:
        """Gets average price data for all known items over the given time filter.

        Args:
            game (`enums.TimeSeriesGameType`): The game type to check prices for.

            time_filter (`enums.RtTimeFilter`): The amount of time to filter on.

            timestamp (`datetime | None`): The time that represents the begining of the
                time period to be averaged.

        Returns:
            `result.Result[models.TimeFilteredPriceResponse, models.ErrorResponse]`:
                A result continaing the price data, or an error if one occurred.
        """

    @abc.abstractmethod
    async def get_avg_price_by_id(
        self, id: int, game: enums.TimeSeriesGameType, timestep: enums.TimeSeriesFilter
    ) -> result.Result[list[models.TimeSeriesPriceResponse], models.ErrorResponse]:
        """Gets the average price data of the item over the given time series.

        Args:
            id (`int`): The item id to get prices for.

            game (`enums.TimeSeriesGameType`): The game type to check prices for.

            timestep (`enums.TimeSeriesFilter`): The timestep to use for calculating averages.

        Returns:
            result.Result[list[models.TimeSeriesPriceResponse], models.ErrorResponse]:
                A result continaing the price data, or an error if one occurred.
        """
