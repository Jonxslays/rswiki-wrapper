from __future__ import annotations

import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import BaseResponse
from rswiki_wrapper import enums

__all__ = (
    "CompressedPriceResponse",
    "ErrorResponse",
    "LatestExchangeUpdateResponse",
    "PaginatedSocialFeedResponse",
    "PaginationMeta",
    "PriceResponse",
    "SocialFeedResponse",
    "VosResponse",
    "VosHistoryResponse",
)


@dataclass(slots=True, init=False)
class ErrorResponse(BaseResponse):
    success: bool
    error: str

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> ErrorResponse:
        self = cls()
        self.success = data["success"]
        self.error = data["error"]
        return self


@dataclass(slots=True, init=False)
class PaginationMeta(BaseResponse):
    has_more: bool
    total_pages: int
    total_items: int

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> PaginationMeta:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, data[attr])

        return self


@dataclass(slots=True, init=False)
class VosResponse(BaseResponse):
    timestamp: datetime
    district1: enums.VosDistrict
    district2: enums.VosDistrict

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
    pagination: PaginationMeta
    data: list[VosResponse]

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> VosHistoryResponse:
        self = cls()
        self.pagination = PaginationMeta.from_raw(data["pagination"])
        self.data = [VosResponse.from_raw(vos) for vos in data["data"]]
        return self


@dataclass(slots=True, init=False)
class LatestExchangeUpdateResponse(BaseResponse):
    rs: datetime
    osrs: datetime
    rs_fsw_2022: datetime
    osrs_fsw_2022: datetime

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> LatestExchangeUpdateResponse:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, self._dt_from_iso(data[attr.replace("_", "-")]))

        return self


@dataclass(slots=True, init=False)
class SocialFeedResponse(BaseResponse):
    id: int
    url: str
    title: str
    excerpt: str
    author: str | None
    curator: str
    source: str | None
    image: str | None
    icon: str | None
    expiry_date: datetime | None
    date_published: datetime | None
    date_added: datetime

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
    pagination: PaginationMeta
    data: list[SocialFeedResponse]

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> PaginatedSocialFeedResponse:
        self = cls()
        self.pagination = PaginationMeta.from_raw(data["pagination"])
        self.data = [SocialFeedResponse.from_raw(feed) for feed in data["data"]]
        return self


@dataclass(slots=True, init=False)
class PriceResponse(BaseResponse):
    id: str
    price: int
    volume: int | None
    timestamp: datetime
    identifier: str

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> PriceResponse:
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
class CompressedPriceResponse(BaseResponse):
    price: int
    timestamp: datetime
    identifier: str

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> CompressedPriceResponse:
        self = cls()

        for key, value in data.items():
            # There should only ever be 1 key in the data passed to this method
            # that contains a 2 item list [epoch timestamp, price]
            self.identifier = key
            self.timestamp = self._dt_from_epoch(value[0], True)
            self.price = value[1]

        return self
