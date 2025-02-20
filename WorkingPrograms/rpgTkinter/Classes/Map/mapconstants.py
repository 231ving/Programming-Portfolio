"""Module for the various Map constants.
"""

from Classes.Rooms.boss_room import BossRoom
from Classes.Rooms.chest_room import ChestRoom
from Classes.Rooms.shop_room import ShopRoom
from Classes.Rooms.combat_room import CombatRoom


class MapConstants:
    """Determines the various constants when generating a new Map.
    """
    TOTAL_ROOMS = 15
    CHANCE_FOR_NEW_EDGE = 0.25
    ROOM_TYPES = {
        "Combat": {
            "desired_number": 10,
            "room": CombatRoom
        },
        "Chest": {
            "desired_number": 2,
            "room": ChestRoom
        },
        "Shop": {
            "desired_number": 2,
            "room": ShopRoom
        },
        "Boss": {
            "desired_number": 1,
            "room": BossRoom
        }
    }
