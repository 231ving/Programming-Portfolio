"""Module containing the unittests for CombatRoom.
"""

import unittest
from Classes.Rooms.combat_room import CombatRoom
from Classes.character import Player, Enemy


class CombatRoomTests(unittest.TestCase):
    """Testcase for CombatRoom.
    """
    def test_1combatroom_init(self):
        """Check that the CombatRoom initializes.
        """
        x = CombatRoom()
        self.assertEqual(x.room_type, "Combat")
        self.assertTrue(x.name)
        self.assertFalse(x.player)
        self.assertFalse(x.is_boss_room)
        self.assertEqual(x.mon_lv, 1)
        self.assertEqual(x.text, "You have entered a Combat room. Prepare to fight.")
        self.assertTrue(x.enemies)
        self.assertEqual(x.enemies_killed, 0)
        for enemy in x.enemies:
            self.assertIsInstance(enemy, Enemy)

    def test_2generate_enemies(self):
        """Check that the CombatRoom correctly generates enemies at LV 1.
        """
        x = CombatRoom()
        self.assertTrue(x.enemies)
        for enemy in x.enemies:
            self.assertEqual(enemy.stats["Level"], 1)

    def test_3generate_enemies_player_exists(self):
        """Check that the CombatRoom correctly generates enemies at player's lv.
        """
        x = CombatRoom()
        player = Player("Default", None)
        player.stats["Level"] = 5
        x.player = player
        x.enemies = []
        x.generate_enemies()
        for enemy in x.enemies:
            self.assertEqual(enemy.stats["Level"], player.stats["Level"])

    def test_4lv_enemies(self):
        """Check that the CombatRoom correctly updates enemy levels.
        """
        x = CombatRoom()
        character = Player("Bob", None)
        character.stats["Level"] = 10
        x.player = character
        x.lv_enemies()
        for enemy in x.enemies:
            self.assertEqual(enemy.stats["Level"], x.player.stats["Level"])
        self.assertEqual(x.player, character)
