from __future__ import annotations

import abc

from .http import HttpContract
from .. import enums
from .. import models
from .. import result

__all__ = ("WeirdGloopContract",)


class WeirdGloopContract(abc.ABC):
    """The contract required to satify the weird gloop API.

    Args:
        http_service (`HttpContract`): The http service to use to satify
            this contract.
    """

    @abc.abstractmethod
    def __init__(self, http_service: HttpContract) -> None:
        ...

    @abc.abstractmethod
    async def get_vos(self) -> models.VosResponse:
        """Gets the current Voice of Seren in RS3, and the time it last updated.

        Returns:
            `models.VosResponse`: The requested VoS data.
        """

    @abc.abstractmethod
    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        """Gets a paginated list of the past history of the Voice of Seren in RS3.

        Args:
            page (`int`): The page of data to retrieve

        Returns:
            `models.VosHistoryResponse`: The list of past VoS and pagination metadata.
                Typically 10 items are included in the history.
        """

    @abc.abstractmethod
    async def get_social_feed(self, page: int) -> models.PaginatedSocialFeedResponse:
        """Gets a paginated list of Runescape related social media posts/items.

        Args:
            page (`int`): The page of data to retrieve

        Returns:
            `models.PaginatedSocialFeedResponse`: The requested posts/articles and
                pagination metadata. Typically 10 items are included in the history.
        """

    @abc.abstractmethod
    async def get_latest_social_feed(self) -> models.SocialFeedResponse:
        """Gets the latest Runescape related social media post/item.

        Returns:
            `models.SocialFeedResponse`: The latest post/article.
        """

    @abc.abstractmethod
    async def get_latest_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        """Gets the timestamp of latest grand exchange update for each game type.

        Returns:
            models.LatestExchangeUpdateResponse: The requested timestamps.
        """

    @abc.abstractmethod
    async def get_latest_price(
        self, game: enums.GameType, *ids_or_names: str | int, locale: enums.Locale | None
    ) -> result.Result[list[models.PriceResponse], models.ErrorResponse]:
        """Gets the latest price for an item(s) by id or name.

        ```py
        # Example
        await client.get_latest_price(GameType.RS, "abyssal whip", "dragon dagger")
        await client.get_latest_price(GameType.RS, 4151, 1215)
        ```

        NOTE:
            If both ids and names are used ids take precedence and none of the names
                will be returned from the API.

        Args:
            game (`enums.GameType`): The game type to check the price on.

            *ids_or_names (`str | int`): The ids as integers, or names as strings to get
                the price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.PriceResponse], models.ErrorResponse]`:
                A result containing either a list of the latest price response models,
                or an error.
        """

    @abc.abstractmethod
    async def get_historical_price(
        self,
        game: enums.GameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.PriceResponse], models.ErrorResponse]:
        """Gets the historical price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.GameType`): The game type to check the price on.

            time_filter (`enums.TimeFilter`): The amount of time to get the history for.

        Keyword Args:
            id (`int | None`): The item id to get the historical price for.

            name (`string | None`): The item name to get the historical price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English. Defaults to None.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.PriceResponse], models.ErrorResponse]`:
                A result containing either a list of the historical price response
                models, or an error.
        """

    @abc.abstractmethod
    async def get_compressed_historical_price(
        self,
        game: enums.GameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.CompressedPriceResponse], models.ErrorResponse]:
        """Gets the compressed historical price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.GameType`): The game type to check the price on.

            time_filter (`enums.TimeFilter`): The amount of time to get the history for.

        Keyword Args:
            id (`int | None`): The item id to get the historical price for.

            name (`string | None`): The item name to get the historical price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English. Defaults to None.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.PriceResponse], models.ErrorResponse]`:
                A result containing either a list of the compressed historical
                price response models, or an error.
        """

    @abc.abstractmethod
    async def get_current_tms(self) -> list[models.TmsResponse]:
        """Gets the current Travelling Merchant Shop items.

        Returns:
            `list[models.TmsResponse]`: The current TMS items.
        """

    @abc.abstractmethod
    async def get_next_tms(self) -> list[models.TmsResponse]:
        """Gets the Travelling Merchant Shop items for tomorrow.

        Returns:
            `list[models.TmsResponse]`: Tomorrow's TMS items.
        """
