"""Module containing the unittests for ChestRoom.
"""
import unittest
from Classes.Rooms.chest_room import ChestRoom
from Classes.item import Item


class ChestRoomTests(unittest.TestCase):
    """Testcase for ChestRoom.
    """

    def test_1chestroom_init(self):
        """Test that the instance is made correctly.
        """
        x = ChestRoom()
        self.assertEqual(x.room_type, "Chest")
        self.assertTrue(x.name)
        self.assertEqual(x.text, "You have entered a Chest room."
                                 " Prepare to open a chest.")
        self.assertTrue(isinstance(x.item, Item))
