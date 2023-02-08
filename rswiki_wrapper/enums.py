from enum import Enum


class BaseUrl(Enum):
    WEIRD_GLOOP_BASE_URL = "https://api.weirdgloop.org"
    MEDIAWIKI_BASE_URL = "https://runescape.wiki/api.php"
    MEDIAWIKI_OSRS_BASE_URL = "https://oldschool.runescape.wiki/api.php"
    REALTIME_WIKI_PRICE_BASE_URL = "https://prices.runescape.wiki/api/v1"


class DefaultHeaders(Enum):
    PROJECT_NAME = "RS Wiki API Python Wrapper"
    CONTACT_INFO = "Default"


class GameType(Enum):
    RS = "rs"
    OSRS = "osrs"
    RS_FSW_2022 = "rs-fsw-2022"
    OSRS_FSW_2022 = "osrs-fsw-2022"


class VosDistrict(Enum):
    AMLODD = "Amlodd"
    CADARN = "Cadarn"
    CRWYS = "Crwys"
    HEFIN = "Hefin"
    IORWERTH = "Iorwerth"
    ITHELL = "Ithell"
    MEILYR = "Meilyr"
    TRAHAEARN = "Trahaearn"
