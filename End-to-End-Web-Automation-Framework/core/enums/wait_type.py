"""Wait type enum for explicit wait strategies."""

from enum import Enum

class WaitType(Enum):
    """Defines supported explicit wait strategies."""
    NONE = "none"
    CLICKABLE = "clickable"
    VISIBLE = "visible"
    PRESENT = "present"
    INVISIBLE = "invisible"
   


