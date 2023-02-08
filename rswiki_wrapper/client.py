from __future__ import annotations

import sys
import typing as t

from rswiki_wrapper import contracts
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result
from rswiki_wrapper import services


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

        http (`contracts.HttpContract | None`): The underlying http service to use for
            requests. Defaults to `None`.

        weird_gloop (`contracts.WeirdGloopContract | None`): The weird gloop service
            to use for weird gloop API calls. Defaults to `None`.
    """

    __slots__ = ("_contact_info", "_http", "_project_name", "_weird_gloop")

    def __init__(
        self,
        project_name: str | None = None,
        contact_info: str | None = None,
        *,
        http: contracts.HttpContract | None = None,
        weird_gloop: contracts.WeirdGloopContract | None = None,
    ) -> None:
        (
            self._assure_headers(project_name, contact_info)
            ._assure_http(http)
            ._assure_weird_gloop(weird_gloop)
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

    async def get_social_feed(self, page: int) -> models.SocialFeedResponse:
        """Gets a paginated list of Runescape related social media posts/items.

        Args:
            page (`int`): The page of data to retrieve

        Returns:
            `models.SocialFeedResponse`: The requested posts/articles and pagination
                metadata. Typically 10 items are included in the history.
        """
        return await self._weird_gloop.get_social_feed(page)

    async def get_latest_price(
        self, game: enums.GameType, *ids_or_names: str | int, locale: enums.Locale | None = None
    ) -> result.Result[list[models.LatestPriceResponse], models.ErrorResponse]:
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
                The locale to use, if `None` the API uses English. Defaults to None.

        Returns:
            `result.Result[list[models.LatestPriceResponse], models.ErrorResponse]`:
                A result containing either a list of the latest price response models,
                or an error.
        """
        return await self._weird_gloop.get_latest_price(game, *ids_or_names, locale=locale)
