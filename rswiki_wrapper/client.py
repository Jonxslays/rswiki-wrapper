from __future__ import annotations

import sys
import typing as t

from rswiki_wrapper import contracts
from rswiki_wrapper import enums
from rswiki_wrapper import models
from rswiki_wrapper import result
from rswiki_wrapper import services


class Client:
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
        return self._project_name

    @project_name.setter
    def project_name(self, project_name: str) -> None:
        self._project_name = project_name

    def _assure_headers(self, project_name: str | None, contact_info: str | None) -> Client:
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
        self._http = http or t.cast(
            contracts.HttpContract, services.HttpService(self._project_name, self._contact_info)
        )

        return self

    def _assure_weird_gloop(self, weird_gloop: contracts.WeirdGloopContract | None) -> Client:
        self._weird_gloop = weird_gloop or t.cast(
            contracts.WeirdGloopContract, services.WeirdGloopService(self._http)
        )

        return self

    async def close(self) -> None:
        await self._http.close()

    async def get_vos(self) -> models.VosResponse:
        return await self._weird_gloop.get_vos()

    async def get_vos_history(self, page: int) -> models.VosHistoryResponse:
        return await self._weird_gloop.get_vos_history(page)

    async def get_latest_exchange_update(self) -> models.LatestExchangeUpdateResponse:
        return await self._weird_gloop.get_latest_exchange_update()

    async def get_social_feed(self, page: int) -> models.SocialFeedResponse:
        return await self._weird_gloop.get_social_feed(page)

    async def get_latest_price(
        self, game: enums.GameType, *, id: int | None = None, name: str | None = None
    ) -> result.Result[models.LatestPriceResponse, models.ErrorResponse]:
        return await self._weird_gloop.get_latest_price(game, id=id, name=name)
