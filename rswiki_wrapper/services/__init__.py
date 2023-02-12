"""The default library contract implementations."""

__all__ = ("HttpService", "MediaWikiService", "RealtimeService", "WeirdGloopService")

from .http import *
from .media_wiki import *
from .realtime_wiki import *
from .weird_gloop import *
