from __future__ import annotations

import abc
import typing as t

# from datetime import datetime

from .http import HttpContract
from rswiki_wrapper import enums

# from rswiki_wrapper import models
# from rswiki_wrapper import result

__all__ = ("MediaWikiContract",)


class MediaWikiContract(abc.ABC):
    """The contract required to satify the MediaWiki API.

    Args:
        http_service (`contracts.HttpContract`): The http service to use to satify
            this contract.
    """

    @abc.abstractmethod
    def __init__(self, http_service: HttpContract) -> None:
        ...

    @abc.abstractmethod
    async def browse(self, subject: str, game: enums.MwGameType) -> dict[str, t.Any]:
        ...
