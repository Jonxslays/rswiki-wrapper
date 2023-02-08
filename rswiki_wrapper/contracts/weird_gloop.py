from __future__ import annotations

import abc

from .http import HttpContract
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result

__all__ = ("WeirdGloopContract",)


class WeirdGloopContract(abc.ABC):
    @abc.abstractmethod
    def __init__(self, http_service: HttpContract) -> None:
        ...

    @abc.abstractmethod
    async def get_vos(self) -> models.VosResponse:
        ...

    @abc.abstractmethod
    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        ...

    @abc.abstractmethod
    async def get_social_feed(self, page: int) -> models.SocialFeedResponse:
        ...

    @abc.abstractmethod
    async def get_latest_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        ...

    @abc.abstractmethod
    async def get_latest_price(
        self, game: enums.GameType, *ids_or_names: str | int, locale: enums.Locale | None
    ) -> result.Result[list[models.LatestPriceResponse], models.ErrorResponse]:
        ...
