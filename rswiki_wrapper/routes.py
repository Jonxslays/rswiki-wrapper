from __future__ import annotations

import typing as t
from dataclasses import dataclass

from rswiki_wrapper.enums import BaseUrl


@dataclass(slots=True)
class CompiledRoute:
    base: BaseUrl
    uri: str
    params: dict[str, str | int]

    def __init__(self, route: Route) -> None:
        self.base = route.base
        self.uri = route.uri
        self.params = {}

    def with_params(self, params: dict[str, str | int]) -> CompiledRoute:
        self.params.update(params)
        return self

    def get_params_str(self) -> str:
        params = ""

        for p, v in self.params.items():
            if params:
                params += f"&{p}={v}"
            else:
                params += f"?{p}={v}"

        return params

    def pretty(self) -> str:
        return self.base.value + self.uri + self.get_params_str()


@dataclass(slots=True, frozen=True)
class Route:
    base: BaseUrl
    uri: str

    def compile(self, *args: str | int) -> CompiledRoute:
        compiled = CompiledRoute(self)

        for arg in args:
            compiled.uri.replace("{}", str(arg), 1)

        return compiled


VOS: t.Final[Route] = Route(BaseUrl.WEIRD_GLOOP, "/runescape/vos")
VOS_HISTORY: t.Final[Route] = Route(BaseUrl.WEIRD_GLOOP, "/runescape/vos/history")
LATEST_EXCHANGE_UPDATE: t.Final[Route] = Route(BaseUrl.WEIRD_GLOOP, "/exchange")
LATEST_PRICE: t.Final[Route] = Route(BaseUrl.WEIRD_GLOOP, "/exchange/history/{}/latest")
SOCIAL_FEED: t.Final[Route] = Route(BaseUrl.WEIRD_GLOOP, "/runescape/social")
