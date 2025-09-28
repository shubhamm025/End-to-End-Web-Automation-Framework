"""Element locator strategy enum for Page Objects."""

from enum import Enum

class IdentificationMode(Enum):
    """Defines element identification strategies used across the framework."""

    XPATH = "xpath"
    CSS = "css"
    ID = "id"
    NAME = "name"


