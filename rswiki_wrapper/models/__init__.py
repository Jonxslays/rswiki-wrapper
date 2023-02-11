"""Models used by the library to encapsulate API data."""

__all__ = (
    "BaseResponse",
    "CompressedExchangePriceResponse",
    "ErrorResponse",
    "ExchangePriceResponse",
    "LatestExchangeUpdateResponse",
    "PaginatedSocialFeedResponse",
    "PaginationMeta",
    "RealtimePriceResponse",
    "SocialFeedResponse",
    "TmsResponse",
    "TmsSearchResponse",
    "TmsSearchFullResponse",
    "VosResponse",
    "VosHistoryResponse",
)

from .base import *
from .media_wiki import *
from .realtime_wiki import *
from .shared import *
from .weird_gloop import *
