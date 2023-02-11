from __future__ import annotations

import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import BaseResponse
from rswiki_wrapper import enums

__all__ = (
    "CompressedExchangePriceResponse",
    "ErrorResponse",
    "ExchangePriceResponse",
    "LatestExchangeUpdateResponse",
    "PaginatedSocialFeedResponse",
    "PaginationMeta",
    "SocialFeedResponse",
    "TmsResponse",
    "TmsSearchResponse",
    "TmsSearchFullResponse",
    "VosResponse",
    "VosHistoryResponse",
)


@dataclass(slots=True, init=False)
class ErrorResponse(BaseResponse):
    """An error returned by the weird gloop API."""

    success: bool
    """Whether the request was succesful, always `False`."""
    error: str
    """The error message."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> ErrorResponse:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, data[attr])

        return self


@dataclass(slots=True, init=False)
class PaginationMeta(BaseResponse):
    """Metadata sent with paginated responses."""

    has_more: bool
    """Whether or not there are more pages."""
    total_pages: int
    """The total number of pages available."""
    total_items: int
    """The total number of items available."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> PaginationMeta:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, data[attr])

        return self


@dataclass(slots=True, init=False)
class VosResponse(BaseResponse):
    """Details the currently active Voice of Seren districts."""

    timestamp: datetime
    """When these districts became active."""
    district1: enums.VosDistrict
    """The first active district."""
    district2: enums.VosDistrict
    """The second active district."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> VosResponse:
        self = cls()
        self.timestamp = datetime.fromisoformat(data["timestamp"].rstrip("Z"))

        for i in range(1, 3):
            district_num = f"district{i}"
            district = getattr(enums.VosDistrict, data[district_num].upper())
            setattr(self, district_num, district.value)

        return self


@dataclass(slots=True, init=False)
class VosHistoryResponse(BaseResponse):
    """A paginated history of the active Voice of Seren districts."""

    pagination: PaginationMeta
    """"The pagination metadata."""
    data: list[VosResponse]
    """A list of the historically active districts."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> VosHistoryResponse:
        self = cls()
        self.pagination = PaginationMeta.from_raw(data["pagination"])
        self.data = [VosResponse.from_raw(vos) for vos in data["data"]]
        return self


@dataclass(slots=True, init=False)
class LatestExchangeUpdateResponse(BaseResponse):
    """The latest grand exchange update time for each game type."""

    rs: datetime
    """Runescape 3's latest update."""
    osrs: datetime
    """Oldschool Runescape's latest update."""
    rs_fsw_2022: datetime
    """Runescape 3 Fresh Start World's latest update."""
    osrs_fsw_2022: datetime
    """Oldschool Runescape Fresh Start World's latest update."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> LatestExchangeUpdateResponse:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, self._dt_from_iso(data[attr.replace("_", "-")]))

        return self


@dataclass(slots=True, init=False)
class SocialFeedResponse(BaseResponse):
    """A Runescape related social media post or article."""

    id: int
    """The post id."""
    url: str
    """The url of the post."""
    title: str
    """The title of the post."""
    excerpt: str
    """An excerpt from the post."""
    author: str | None
    """The post's author, may be `None`."""
    curator: str
    """The curator of the post."""
    source: str | None
    """The source of the post, may be `None`."""
    image: str | None
    """An image of/from the post, may be `None`."""
    icon: str | None
    """The icon for the post, may be `None`"""
    expiry_date: datetime | None
    """The expiry date of the post, may be `None`."""
    date_published: datetime | None
    """The date the post was published, may be `None`."""
    date_added: datetime
    """The date the post was added to the API database."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> SocialFeedResponse:
        self = cls()
        self.expiry_date = self._dt_from_iso_maybe(data.pop("expiryDate", None))
        self.date_published = self._dt_from_iso_maybe(data.pop("datePublished", None))
        self.date_added = self._dt_from_iso(data.pop("dateAdded"))

        for k, v in data.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                # Because we iterate the api response items this can fail
                # if the api adds items that don't exist on the model
                pass

        return self


@dataclass(slots=True, init=False)
class PaginatedSocialFeedResponse(BaseResponse):
    """A paginated list of social media posts/articles."""

    pagination: PaginationMeta
    """The pagination metadata."""
    data: list[SocialFeedResponse]
    """A list containing the posts."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> PaginatedSocialFeedResponse:
        self = cls()
        self.pagination = PaginationMeta.from_raw(data["pagination"])
        self.data = [SocialFeedResponse.from_raw(feed) for feed in data["data"]]
        return self


@dataclass(slots=True, init=False)
class ExchangePriceResponse(BaseResponse):
    """The grand exchange price information for an item."""

    id: str
    """The items id."""
    price: int
    """The items price."""
    volume: int | None
    """The items volume traded, or `None`."""
    timestamp: datetime
    """The timestamp for this price."""
    identifier: str
    """The item id as a string, or the item name.
        - depends how this price was searched.
    """

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> ExchangePriceResponse:
        self = cls()

        for attr in self.__dataclass_fields__:
            if attr == "identifier":
                continue

            value = data[attr]
            if attr == "timestamp":
                if isinstance(value, int):
                    value = self._dt_from_epoch(value, True)
                else:
                    value = self._dt_from_iso(value)

            setattr(self, attr, value)

        return self


@dataclass(slots=True, init=False)
class CompressedExchangePriceResponse(BaseResponse):
    """The compressed (less information) price of an item."""

    price: int
    """The items price."""
    timestamp: datetime
    """The timestamp for this price."""
    identifier: str
    """The item id as a string, or the item name.
        - depends how this price was searched.
    """

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> CompressedExchangePriceResponse:
        self = cls()

        for key, value in data.items():
            # There should only ever be 1 key in the data passed to this method
            # that contains a 2 item list [epoch timestamp, price]
            self.identifier = key
            self.timestamp = self._dt_from_epoch(value[0], True)
            self.price = value[1]

        return self


@dataclass(slots=True, init=False)
class TmsResponse(BaseResponse):
    """A Travelling Merchant Shop item."""

    id: int
    """The item id."""
    en: str
    """The item name in English."""
    pt: str
    """The item name in Portuguese."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> TmsResponse:
        self = cls()
        self.id = int(data["id"])
        self.en = data["en"]
        self.pt = data["pt"]
        return self


@dataclass(slots=True, init=False)
class TmsSearchResponse(BaseResponse):
    """A Travelling Merchant Shop search response."""

    date: datetime
    """The date this item was in the Travelling Merchant Shop."""
    items: list[str]
    """The items in the shop on that day (could be either names or ids)."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> TmsSearchResponse:
        self = cls()
        self.items = data["items"]

        try:
            self.date = self._dt_from_strp(data["date"])
        except ValueError:
            # This date is in portuguese
            self.date = self._dt_from_pt(data["date"])

        return self


@dataclass(slots=True, init=False)
class TmsSearchFullResponse(BaseResponse):
    """A Travelling Merchant Shop search full response."""

    date: datetime
    """The date this item was in the Travelling Merchant Shop."""
    items: list[TmsResponse]
    """The items in the shop on that day in English and Portuguese."""

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> TmsSearchFullResponse:
        self = cls()
        self.items = [TmsResponse.from_raw(item) for item in data["items"]]

        try:
            self.date = self._dt_from_strp(data["date"])
        except ValueError:
            # This date is in portuguese
            self.date = self._dt_from_pt(data["date"])

        return self
