"""Enum for supported browser types used by BrowserFactory."""

from enum import Enum


class BrowserType(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"


