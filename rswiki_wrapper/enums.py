"""Various enums used by the library."""

from enum import Enum


class BaseEnum(Enum):
    """The base enum all library enums inherit from."""

    value: str  # type: ignore
    """The value of the enum member."""


class BaseUrl(BaseEnum):
    """Base URL's for the API's we communicate with."""

    WEIRD_GLOOP = "https://api.weirdgloop.org"
    MEDIAWIKI = "https://runescape.wiki/api.php"
    MEDIAWIKI_OSRS = "https://oldschool.runescape.wiki/api.php"
    REALTIME_WIKI_PRICE = "https://prices.runescape.wiki/api/v1"


class DefaultHeaders(BaseEnum):
    """The default user agent used by this library."""

    PROJECT_NAME = "RS Wiki API Python Wrapper"
    CONTACT_INFO = "Default"


class WgGameType(BaseEnum):
    """The game types available on the Weird Gloop API."""

    RS = "rs"
    """Runescape 3"""
    OSRS = "osrs"
    """Oldschool Runescape"""
    RS_FSW_2022 = "rs-fsw-2022"
    """Runescape 3 Fresh Start World"""
    OSRS_FSW_2022 = "osrs-fsw-2022"
    """Oldschool Runescape Fresh Start World"""


class Locale(BaseEnum):
    """A locale for use with some endpoints."""

    EN = "en"
    """English"""
    PT = "pt"
    """Portuguese"""


class RtGameType(BaseEnum):
    """The game types available on the Realtime Wiki API."""

    OSRS = "osrs"
    """Oldschool Runescape"""
    DMM = "dmm"
    """Deadman Mode"""
    FSW = "fsw"
    """Fresh start world"""


class RtTimeFilter(BaseEnum):
    """A length of time to filter by for the realtime API."""

    FIVE_MINS = "5m"
    ONE_HOUR = "1h"


class TimeSeriesFilter(BaseEnum):
    """A length of time to filter by for the realtime API timeseries endpoint."""

    FIVE_MINS = "5m"
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"


class TimeSeriesGameType(BaseEnum):
    """The game types available on the Realtime Wiki API timeseries endpoints."""

    OSRS = "osrs"
    """Oldschool Runescape"""
    FSW = "fsw"
    """Fresh start world"""


class WgTimeFilter(BaseEnum):
    """A length of time to filter by for the weird gloop API."""

    ALL = "all"
    SAMPLE = "sample"
    LAST_90_DAYS = "last90d"


class VosDistrict(BaseEnum):
    """The 8 Voice of Seren discricts."""

    AMLODD = "Amlodd"
    CADARN = "Cadarn"
    CRWYS = "Crwys"
    HEFIN = "Hefin"
    IORWERTH = "Iorwerth"
    ITHELL = "Ithell"
    MEILYR = "Meilyr"
    TRAHAEARN = "Trahaearn"
