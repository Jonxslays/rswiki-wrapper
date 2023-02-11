from __future__ import annotations

import abc

from .http import HttpContract
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result

__all__ = ("RealtimeContract",)


class RealtimeContract(abc.ABC):
    """The contract required to satify the realtime wiki API.

    Args:
        http_service (`HttpContract`): The http service to use to satify
            this contract.
    """

    @abc.abstractmethod
    def __init__(self, http_service: HttpContract) -> None:
        ...

    @abc.abstractmethod
    async def get_realtime_price(
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
