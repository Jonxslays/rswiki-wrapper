"""Library contracts that can be subclassed for custom user defined implementations."""

__all__ = ("HttpContract", "RealtimeContract", "WeirdGloopContract")

from .http import *
from .realtime_wiki import *
from .weird_gloop import *
