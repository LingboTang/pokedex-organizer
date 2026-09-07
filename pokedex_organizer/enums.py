from enum import Enum


class UserBehavior(str, Enum):
    """How the player mainly uses their Pokémon; drives which stats matter most."""

    RAID = "RAID"
    COLLECTION = "COLLECTION"
    GYM = "GYM"
    CASUAL = "CASUAL"
