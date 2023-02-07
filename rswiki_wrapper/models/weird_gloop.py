from __future__ import annotations

import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import BaseResponse
from rswiki_wrapper import enums

__all__ = (
    "ErrorResponse",
    "LatestExchangeUpdateResponse",
    "PaginationMeta",
    "SocialFeedData",
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

    def _from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> LatestExchangeUpdateResponse:
        self = cls()

        for attr in self.__dataclass_fields__:
            setattr(self, attr, self._from_iso(data[attr.replace("_", "-")]))

        return self


@dataclass(slots=True, init=False)
class SocialFeedData(BaseResponse):
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

    def _from_iso(self, timestamp: str | None) -> datetime | None:
        return datetime.fromisoformat(timestamp.rstrip("Z")) if timestamp else None

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> SocialFeedData:
        self = cls()
        self.expiry_date = self._from_iso(data.pop("expiryDate", None))
        self.date_published = self._from_iso(data.pop("datePublished", None))
        self.date_added = t.cast(datetime, self._from_iso(data.pop("dateAdded", None)))

        for k, v in data.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                # Because we iterate the api response items this can fail
                # if the api adds items that don't exist on the model
                pass

        return self


@dataclass(slots=True, init=False)
class SocialFeedResponse(BaseResponse):
    pagination: PaginationMeta
    data: list[SocialFeedData]

    @classmethod
    def from_raw(cls, data: dict[str, t.Any]) -> SocialFeedResponse:
        self = cls()
        self.pagination = PaginationMeta.from_raw(data["pagination"])
        self.data = [SocialFeedData.from_raw(feed) for feed in data["data"]]
        return self
