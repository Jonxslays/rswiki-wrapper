from __future__ import annotations

import json
import typing as t

# from datetime import datetime

from rswiki_wrapper import contracts
from rswiki_wrapper import enums

# from rswiki_wrapper import models
# from rswiki_wrapper import result
from rswiki_wrapper import routes

__all__ = ("MediaWikiService",)


@t.final
class MediaWikiService(contracts.MediaWikiContract):
    __slots__ = ("_http",)

    def __init__(self, http_service: contracts.HttpContract) -> None:
        self._http = http_service

    async def _fetch(self, route: routes.CompiledRoute) -> dict[str, t.Any]:
        return await self._http.fetch(route)

    def _build_params(self, **params: t.Any) -> dict[str, str | int]:
        return {
            "action": "smwbrowse",
            "format": "json",
            "browse": "subject",
            "params": json.dumps({"limit": 20, "fullText": True, "ns": 0, **params}),
        }

    def _apply_url_update(self, game: enums.MwGameType, route: routes.CompiledRoute) -> None:
        if game is enums.MwGameType.OSRS:
            route.base = enums.BaseUrl.MEDIAWIKI_OSRS

    # Example:
    # https://runescape.wiki/api.php?action=smwbrowse&format=json&browse=subject&params={"subject":"legends quest","limit":20,"fullText":true,"ns":0}
    async def browse(self, subject: str, game: enums.MwGameType) -> dict[str, t.Any]:
        params = self._build_params(subject=subject)
        route = routes.MEDIAWIKI.compile().with_params(params)
        self._apply_url_update(game, route)
        data = await self._fetch(route)
        return data
