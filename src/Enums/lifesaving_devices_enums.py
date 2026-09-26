import enum


class RescueAssetType(enum.Enum):
    SHIP = "судно"
    TUG = "буксир"
    BOAT = "катер"
    HOVERCRAFT = "СВП"
    HELICOPTER = "вертолет"


class RescueAssetStatus(enum.Enum):
    READY = "готов"
    ON_MISSION = "в рейде"
    UNDER_MAINTENANCE = "на обслуживании"