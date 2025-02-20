"""Module containing the unittests for BossRoom.
"""

import unittest
from Classes.Rooms.boss_room import BossRoom


class BossRoomTests(unittest.TestCase):
    """Testcase for the BossRoom.
    """

    def test_1bossroom_init(self):
        """Check that the BossRoom initializes.
        """
        x = BossRoom()
        self.assertEqual(x.room_type, "Boss")
        self.assertTrue(x.name)
        self.assertTrue(x.is_boss_room)
        self.assertEqual(x.enemies_killed, 0)
        self.assertTrue(x.enemies)
        self.assertEqual(x.enemies[0].name, "BOSS")

    def test_2lv_boss(self):
        """Check that the lv_boss method works.
        """
        x = BossRoom()
        enemy_attack = x.enemies[0].attack
        enemy_defense = x.enemies[0].defense

        x.lv_boss(5)
        for enemy in x.enemies:
            self.assertEqual(enemy.stats["Level"], 10)
            self.assertEqual(enemy.stats["Stat Points"], 0)
            self.assertTrue(enemy.attack > enemy_attack)
            self.assertTrue(enemy.defense > enemy_defense)
