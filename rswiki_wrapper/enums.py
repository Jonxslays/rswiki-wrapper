from enum import Enum


class BaseUrl(Enum):
    WEIRD_GLOOP = "https://api.weirdgloop.org"
    MEDIAWIKI = "https://runescape.wiki/api.php"
    MEDIAWIKI_OSRS = "https://oldschool.runescape.wiki/api.php"
    REALTIME_WIKI_PRICE = "https://prices.runescape.wiki/api/v1"


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
