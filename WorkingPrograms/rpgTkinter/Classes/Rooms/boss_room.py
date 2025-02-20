"""Module for the BossRoom class.
"""

from Classes.Rooms.room import Room
from Classes.character import Enemy


class BossRoom(Room):
    """Acts similarly to CombatRoom.
    """
    def __init__(self):
        """Creates the instance.
        """
        super().__init__()
        self.name = self.generate_name("Combat")
        self.room_type = "Boss"
        self.enemies_killed = 0

        # mon_name = random.choice(CombatRoom.ENEMIES)
        self.mon_name = "BOSS"

        self.is_boss_room = True
        self.enemies = [Enemy(self.mon_name, None, 5)]

    def lv_boss(self, lv_change: int):
        """Method to level up the boss associated with the Boss Room.
        Args:
            lv_change (int): How many levels to increase the boss by.
         """
        for enemy in self.enemies:
            enemy.stats["Level"] += lv_change
            enemy.stats["Stat Points"] = lv_change * 5
            enemy.update_stats()
            enemy.stats["Health"] = enemy.stats["Max Health"]
            enemy.update_attack()
            enemy.update_defense()
