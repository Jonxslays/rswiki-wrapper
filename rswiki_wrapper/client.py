"""The client implementation used by the library."""

from __future__ import annotations

import sys
import typing as t
from datetime import datetime

from rswiki_wrapper import contracts
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result
from rswiki_wrapper import services

__all__ = ("Client",)


class Client:
    """The core interface used to make API requests.

    If any of the below arguments are `None`, a default library provided
    implementation will be used. Custom user defined implementations can be used
    as well, as long as they satify the associated contract.

    A warning will be issued if either of `project_name` or `contact_info` is not set.

    Args:
        project_name (`str | None`): The project name to use in the request headers.
            Defaults to `None`.

        contact_info (`str | None`): The contact info to use in the request headers.
            Defaults to `None`.

    Keyword Args:
        http (`contracts.HttpContract | None`): The underlying http service to use for
            requests. Defaults to `None`.

        weird_gloop (`contracts.WeirdGloopContract | None`): The weird gloop service
            to use for weird gloop API calls. Defaults to `None`.

        realtime (`contracts.RealtimeContract | None`): The realtime service
            to use for realtime wiki API calls. Defaults to `None`.
    """

    __slots__ = ("_contact_info", "_http", "_project_name", "_realtime", "_weird_gloop")

    def __init__(
        self,
        project_name: str | None = None,
        contact_info: str | None = None,
        *,
        http: contracts.HttpContract | None = None,
        weird_gloop: contracts.WeirdGloopContract | None = None,
        realtime: contracts.RealtimeContract | None = None,
    ) -> None:
        (
            self._assure_headers(project_name, contact_info)
            ._assure_http(http)
            ._assure_weird_gloop(weird_gloop)
            ._assure_realtime(realtime)
        )

    @property
    def contact_info(self) -> str:
        """The contact info being sent with request headers."""
        return self._contact_info

    @contact_info.setter
    def contact_info(self, contact_info: str) -> None:
        self._contact_info = contact_info

    @property
    def project_name(self) -> str:
        """The project name being sent with request headers."""
        return self._project_name

    @project_name.setter
    def project_name(self, project_name: str) -> None:
        self._project_name = project_name

    def _assure_headers(self, project_name: str | None, contact_info: str | None) -> Client:
        """Uses the user defined values or sets the default request headers.

        A warning will be issued if the user does not set any headers.

        Args:
            project_name (`str | None`): The project name to use in the user agent header.

            contact_info (`str | None`): The contact info to use in the user agent header.

        Returns:
            `Client`: The client for chained calls.
        """
        warn: t.Callable[[str], None] = lambda attr: print(
            f"{attr} should be set to identify yourself with the API.",
            file=sys.stderr,
        )

        if not project_name:
            warn("Project name")
            project_name = enums.DefaultHeaders.PROJECT_NAME.value

        if not contact_info:
            warn("Contact info")
            contact_info = enums.DefaultHeaders.CONTACT_INFO.value

        self._project_name = project_name
        self._contact_info = contact_info
        return self

    def _assure_http(self, http: contracts.HttpContract | None) -> Client:
        """Uses the user defined http service, if provided. Otherwise instantiates the
        default implementation.

        Args:
            http (`contracts.HttpContract | None`): The http service that inherits the
                http contract, or `None` if the default should be used.

        Returns:
            `Client`: The client for chained calls.
        """
        self._http = http or t.cast(
            contracts.HttpContract, services.HttpService(self._project_name, self._contact_info)
        )

        return self

    def _assure_weird_gloop(self, weird_gloop: contracts.WeirdGloopContract | None) -> Client:
        """Uses the user defined weird gloop service, if provided. Otherwise
        instantiates the default implementation.

        Args:
            weird_gloop (`contracts.WeirdGloopContract | None`): The weird gloop service
                that inherits the weird gloop contract, or `None` if the default should
                be used.

        Returns:
            `Client`: The client for chained calls.
        """
        self._weird_gloop = weird_gloop or t.cast(
            contracts.WeirdGloopContract, services.WeirdGloopService(self._http)
        )

        return self

    def _assure_realtime(self, realtime: contracts.RealtimeContract | None) -> Client:
        """Uses the user defined realtime service, if provided. Otherwise
        instantiates the default implementation.

        Args:
            realtime (`contracts.RealtimeContract | None`): The realtime service
                that inherits realtime contract, or `None` if the default should
                be used.

        Returns:
            `Client`: The client for chained calls.
        """
        self._realtime = realtime or t.cast(
            contracts.RealtimeContract, services.RealtimeService(self._http)
        )

        return self

    async def close(self) -> None:
        """Closes the in use http client session.

        Required before the program terminates to avoid a warning.
        """
        await self._http.close()

    async def get_vos(self) -> models.VosResponse:
        """Gets the current Voice of Seren in RS3, and the time it last updated.

        Returns:
            `models.VosResponse`: The requested VoS data.
        """
        return await self._weird_gloop.get_vos()

    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        """Gets a paginated list of the past history of the Voice of Seren in RS3.

        Args:
            page (`int`): The page of data to retrieve

        Returns:
            `models.VosHistoryResponse`: The list of past VoS and pagination metadata.
                Typically 10 items are included in the history.
        """
        return await self._weird_gloop.get_vos_history(page)

    async def get_latest_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        """Gets the timestamp of latest grand exchange update for each game type.

        Returns:
            models.LatestExchangeUpdateResponse: The requested timestamps.
        """
        return await self._weird_gloop.get_latest_exchange_update()

    async def get_social_feed(self, page: int) -> models.PaginatedSocialFeedResponse:
        """Gets a paginated list of Runescape related social media posts/items.

        Args:
            page (`int`): The page of data to retrieve

        Returns:
            `models.PaginatedSocialFeedResponse`: The requested posts/articles and
                pagination metadata. Typically 10 items are included in the history.
        """
        return await self._weird_gloop.get_social_feed(page)

    async def get_latest_social_feed(self) -> models.SocialFeedResponse:
        """Gets the latest Runescape related social media post/item.

        Returns:
            `models.SocialFeedResponse`: The latest post/article.
        """
        return await self._weird_gloop.get_latest_social_feed()

    async def get_latest_exchange_price(
        self, game: enums.WgGameType, *ids_or_names: str | int, locale: enums.Locale | None = None
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

        Keyword Args:
            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English. Defaults to None.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]`:
                A result containing either a list of the latest price response models,
                or an error.
        """
        return await self._weird_gloop.get_latest_exchange_price(
            game, *ids_or_names, locale=locale
        )

    async def get_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None = None,
        name: str | None = None,
        locale: enums.Locale | None = None,
    ) -> result.Result[list[models.ExchangePriceResponse], models.ErrorResponse]:
        """Gets the historical grand exchange price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.WgGameType`): The game type to check the price on.

            time_filter (`enums.TimeFilter`): The amount of time to get the history for.

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
        return await self._weird_gloop.get_historical_exchange_price(
            game, time_filter, id=id, name=name, locale=locale
        )

    async def get_compressed_historical_exchange_price(
        self,
        game: enums.WgGameType,
        time_filter: enums.TimeFilter,
        *,
        id: int | None = None,
        name: str | None = None,
        locale: enums.Locale | None = None,
    ) -> result.Result[list[models.CompressedExchangePriceResponse], models.ErrorResponse]:
        """Gets the compressed historical grand exchange price for an item by id or name.

        NOTE:
            If both id and name are passed to this function, id will take precedence.

        Args:
            game (`enums.WgGameType`): The game type to check the price on.

            time_filter (`enums.TimeFilter`): The amount of time to get the history for.

        Keyword Args:
            id (`int | None`): The item id to get the historical price for.

            name (`string | None`): The item name to get the historical price for.

            locale (`enums.Locale | None`):
                The locale to use, if `None` the API uses English. Defaults to None.
                    Only useful if names were used.

        Returns:
            `result.Result[list[models.CompressedExchangePriceResponse], models.ErrorResponse]`:
                A result containing either a list of the compressed historical
                price response models, or an error.
        """
        return await self._weird_gloop.get_compressed_historical_exchange_price(
            game, time_filter, id=id, name=name, locale=locale
        )

    async def get_current_tms(self) -> list[models.TmsResponse]:
        """Gets the current Travelling Merchant Shop items.

        Returns:
            `list[models.TmsResponse]`: The current TMS items.
        """
        return await self._weird_gloop.get_current_tms()

    async def get_next_tms(self) -> list[models.TmsResponse]:
        """Gets the Travelling Merchant Shop items for tomorrow.

        Returns:
            `list[models.TmsResponse]`: Tomorrow's TMS items.
        """
        return await self._weird_gloop.get_next_tms()

    async def search_tms_by_name(
        self,
        *names: str,
        locale: enums.Locale | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        count: int | None = None,
    ) -> result.Result[list[models.TmsSearchResponse], models.ErrorResponse]:
        """Searches for item(s) in the Travelling Merchant Shop history by name.

        ```py
        # Example
        await client.get_latest_price(
            "Slayer VIP Coupon", "Harmonic Dust", locale=enums.Locale.EN
        )

        await client.get_latest_price("Cristal de anima", locale=enums.Locale.PT)
        ```

        Args:
            *names: (`str`): The names to search for. For some reason this API endpoint
                is really picky about capitalization, so be wary of that.

        Keyword Args:
            locale (`enums.Locale | None`): The locale to use. Will use English if `None`.
                Defaults to `None`.

            start_at (`datetime | None`): The date to begin the search at. Defaults to `None`.

            end_at (`datetime | None`): The date to end the search at. Only this or `count`
                should be specified, never both. Defaults to `None`.

            count: (`int | None`): The total number of results to return. Only this or `end_at`
                should be specified, never both. Defaults to `None`.

        Returns:
            `result.Result[list[models.TmsSearchResponse], models.ErrorResponse]`:
                A list of the items if found, or an error.
        """
        return await self._weird_gloop.search_tms_by_name(
            *names, locale=locale, start_at=start_at, end_at=end_at, count=count
        )

    async def search_tms_by_id(
        self,
        *ids: int,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        count: int | None = None,
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
        return await self._weird_gloop.search_tms_by_id(
            *ids, start_at=start_at, end_at=end_at, count=count
        )

    async def search_tms_by_id_full(
        self,
        *ids: int,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        count: int | None = None,
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
        return await self._weird_gloop.search_tms_by_id_full(
            *ids, start_at=start_at, end_at=end_at, count=count
        )

    async def get_realtime_price(
        self, id: int | None = None, game: enums.RtGameType = enums.RtGameType.OSRS
    ) -> result.Result[list[models.RealtimePriceResponse], models.ErrorResponse]:
        """Gets the latest realtime price data from Runelite.

        NOTE:
            Consider fetching all prices once, and caching them for a period of time.
            Then just do cache lookups for individual ID's. Reduces stress on the API.

        Args:
            id (`int | None`): The item id to search for. If `None`, all known items
                are returned. Defaults to `None`.

            game (`enums.RtGameType`): The game type to get the prices for. Defaults to OSRS.

        Returns:
            `result.Result[list[models.RealtimePriceResponse], models.ErrorResponse]`:
                A result containing the list of prices, or an error.
        """
        return await self._realtime.get_realtime_price(game, id)
