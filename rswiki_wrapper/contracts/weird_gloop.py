from __future__ import annotations

import abc
from datetime import datetime

from .http import HttpContract
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result

__all__ = ("WeirdGloopContract",)


class WeirdGloopContract(abc.ABC):
    """The contract required to satify the weird gloop API.

    Args:
        http_service (`contracts.HttpContract`): The http service to use to satify
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
    async def get_latest_exchange_price(
        self, game: enums.WgGameType, *ids_or_names: str | int, locale: enums.Locale | None
    ) -> result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]:
        """Gets the latest grand exchange price for an item(s) by id or name.

        ```py
        # Example
        await client.get_latest_exchange_price(GameType.RS, "abyssal whip", "dragon dagger")
        await client.get_latest_exchange_price(GameType.RS, 4151, 1215)
        ```

        NOTE:
            If both ids and names are used ids take precedence and none of the names
                will be returned from the API.

        Args:
            game (`enums.WgGameType`): The game type to check the price on.

            *ids_or_names (`str | int`): The ids as integers, or names as strings to get
                the price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]`:
                A result containing either a list of the latest price response models,
                or an error.
        """

    @abc.abstractmethod
    async def get_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.WgTimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]:
        """Gets the historical grand exchange price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.WgGameType`): The game type to check the price on.

            time_filter (`enums.WgTimeFilter`): The amount of time to get the history for.

        Keyword Args:
            id (`int | None`): The item id to get the historical price for.

            name (`string | None`): The item name to get the historical price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English. Defaults to None.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]`:
                A result containing either a list of the historical price response
                models, or an error.
        """

    @abc.abstractmethod
    async def get_compressed_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.WgTimeFilter,
        *,
        id: int | None,
        name: str | None,
        locale: enums.Locale | None,
    ) -> result.Result[list[models.CompressedExchangePriceResponse], models.ErrorResponse]:
        """Gets the compressed historical grand exchange price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.WgGameType`): The game type to check the price on.

            time_filter (`enums.WgTimeFilter`): The amount of time to get the history for.

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

    @abc.abstractmethod
    async def search_tms_by_name(
        self,
        *names: str,
        locale: enums.Locale | None,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchResponse], models.ErrorResponse]:
        """Searches for item(s) in the Travelling Merchant Shop history and future
        stock by name.

        ```py
        # Example
        await client.search_tms_by_name(
            "Slayer VIP Coupon", "Harmonic Dust", locale=enums.Locale.EN
        )

        await client.search_tms_by_name("Cristal de anima", locale=enums.Locale.PT)
        ```

        Args:
            *names: (`str`): The names to search for. For some reason this API endpoint
                is really picky about capitalization, so be wary of that.

        Keyword Args:
            locale (`enums.Locale | None`): The locale to use. Will use English if `None`.

            start_at (`datetime | None`): The date to begin the search at.

            end_at (`datetime | None`): The date to end the search at. Only this or `count`
                should be specified, never both.

            count: (`int | None`): The total number of results to return. Only this or `end_at`
                should be specified, never both.

        Returns:
            `result.Result[list[models.TmsSearchResponse], models.ErrorResponse]`:
                A list of the items if found, or an error.
        """

    @abc.abstractmethod
    async def search_tms_by_id(
        self,
        *ids: int,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchResponse], models.ErrorResponse]:
        """Searches for item(s) in the Travelling Merchant Shop history and future
        stock by id.

        ```py
        # Example
        await client.search_tms_by_id(42274, 34918)
        ```

        Args:
            *ids: (`int`): The ids to search for.

        Keyword Args:
            start_at (`datetime | None`): The date to begin the search at.

            end_at (`datetime | None`): The date to end the search at. Only this or `count`
                should be specified, never both.

            count: (`int | None`): The total number of results to return. Only this or `end_at`
                should be specified, never both.

        Returns:
            `result.Result[list[models.TmsSearchResponse], models.ErrorResponse]`:
                A list of the items if found, or an error.
        """

    @abc.abstractmethod
    async def search_tms_by_id_full(
        self,
        *ids: int,
        start_at: datetime | None,
        end_at: datetime | None,
        count: int | None,
    ) -> result.Result[list[models.TmsSearchFullResponse], models.ErrorResponse]:
        """Searches for item(s) in the Travelling Merchant Shop history and future
        stock by id. Returns both English and Portuguese names.

        ```py
        # Example
        await client.search_tms_by_id_full(42274, 34918)
        ```

        Args:
            *ids: (`int`): The ids to search for.

        Keyword Args:
            start_at (`datetime | None`): The date to begin the search at.

            end_at (`datetime | None`): The date to end the search at. Only this or `count`
                should be specified, never both.

            count: (`int | None`): The total number of results to return. Only this or `end_at`
                should be specified, never both.

        Returns:
            `result.Result[list[models.TmsSearchFullResponse], models.ErrorResponse]`:
                A list of the items if found, or an error.
        """
