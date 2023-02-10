"""Contracts that can be subclassed for custom user defined implementations."""

__all__ = ("HttpContract", "WeirdGloopContract")

from .http import *
from .weird_gloop import *
