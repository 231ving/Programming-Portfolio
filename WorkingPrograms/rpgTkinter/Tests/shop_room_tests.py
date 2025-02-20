"""Module containing the unittests for the ShopRoom class.
"""
import unittest
from Classes.Rooms.shop_room import ShopRoom
from Classes.item import Item


class ShopRoomTests(unittest.TestCase):
    """Testcase for the ShopRoom class.
    """
    def test_1shoproom_init(self):
        """Test for the ShopRoom initialization.
        """
        x = ShopRoom()
        self.assertEqual(x.room_type, "Shop")
        self.assertTrue(x.name)
        self.assertEqual(x.text, "You have entered a Shop room."
                                 " Prepare to buy items.")
        self.assertTrue(x.items)
        for item in x.items:
            self.assertIsInstance(item, Item)
        self.assertTrue(1 <= len(x.items) <= 4)
