from enum import Enum


class BaseUrl(Enum):
    """Base URL's for the API's we communicate with."""

    WEIRD_GLOOP = "https://api.weirdgloop.org"
    MEDIAWIKI = "https://runescape.wiki/api.php"
    MEDIAWIKI_OSRS = "https://oldschool.runescape.wiki/api.php"
    REALTIME_WIKI_PRICE = "https://prices.runescape.wiki/api/v1"


class DefaultHeaders(Enum):
    """The default user agent used by this library."""

    PROJECT_NAME = "RS Wiki API Python Wrapper"
    CONTACT_INFO = "Default"


class GameType(Enum):
    """Various Runescape game types."""

    RS = "rs"
    """Runescape 3"""
    OSRS = "osrs"
    """Oldschool Runescape"""
    RS_FSW_2022 = "rs-fsw-2022"
    """Runescape 3 Fresh Start World"""
    OSRS_FSW_2022 = "osrs-fsw-2022"
    """Oldschool Runescape Fresh Start World"""


class Locale(Enum):
    """A locale for use with some endpoints."""

    EN = "en"
    """English"""
    PT = "pt"
    """Portuguese"""


class TimeFilter(Enum):
    """A length of time to filter by."""

    ALL = "all"
    SAMPLE = "sample"
    LAST_90_DAYS = "last90d"


class TmsQuery(Enum):
    """Query options for the Travelling Merchant Shop."""

    EN = "en"
    """The item names in English."""
    PT = "pt"
    """The item names in Portuguese."""
    ID = "id"
    """The item id's"""
    FULL = "full"
    """The item names and id's in both English and Portuguese."""


class VosDistrict(Enum):
    """The 8 Voice of Seren discricts."""

    AMLODD = "Amlodd"
    CADARN = "Cadarn"
    CRWYS = "Crwys"
    HEFIN = "Hefin"
    IORWERTH = "Iorwerth"
    ITHELL = "Ithell"
    MEILYR = "Meilyr"
    TRAHAEARN = "Trahaearn"
