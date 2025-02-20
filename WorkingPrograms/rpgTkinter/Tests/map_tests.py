"""Module containing the unittests for the Map class.
"""
import unittest
from Classes.Map.map import Map
from Classes.Map.edge import Edge
from Classes.Rooms.room import Room
from Classes.Rooms.start_room import StartRoom


class MapTests(unittest.TestCase):
    """Testcase for the Map class.
    """
    def test1_map_init(self):
        """Test that the Map initializes correctly.
        """
        test_map = Map()
        for room in test_map.rooms:
            self.assertIsInstance(room, Room)
        for edge in test_map.edges:
            self.assertIsInstance(edge, Edge)
        self.assertEqual(test_map.current_room, test_map.start_room)
        self.assertIsInstance(test_map.start_room, StartRoom)

    def test2_generate_map(self):
        """Test that the initial instance attributes are correct.
        """
        test_map = Map()
        rooms = test_map.rooms
        edges = []
        current_room = test_map.current_room
        test_map.generate_map()
        self.assertTrue(test_map.rooms != rooms)
        self.assertEqual(test_map.edges, edges)
        self.assertEqual(test_map.current_room, current_room)
        for room in test_map.rooms:
            self.assertTrue(room.get_adjacent_rooms())
        self.assertEqual(test_map.start_room.get_adjacent_rooms(),
                         test_map.get_current_room().get_adjacent_rooms())

    def test3_get_current_room(self):
        """Test the get_current_room method works."""
        test_map = Map()
        self.assertEqual(test_map.get_current_room(), test_map.current_room)

    def test4_set_current_room(self):
        """Test the set_current_room method works."""
        test_map = Map()
        test_map.set_current_room(test_map.rooms[10])
        self.assertEqual(test_map.get_current_room(), test_map.rooms[10])

    def test5_generate_random_rooms(self):
        """Tests the generate_random_rooms method."""
        test_map = Map()
        rooms = test_map.rooms
        test_map.generate_random_rooms()
        self.assertTrue(test_map.rooms != rooms)
        for room in test_map.rooms:
            self.assertIsInstance(room, Room)

    def test6_connect_every_room_together(self):
        """Tests the connect_every_room_together method."""
        test_map = Map()
        test_map.connect_every_room_together()
        for edge in test_map.edges:
            self.assertIsInstance(edge, Edge)

    def test7_prims_algorithm(self):
        """prim's algorithm: Test not implemented"""
        self.skipTest("Test not implemented yet")

    def test8_assign_random_images(self):
        """Test the assign_random_images method for round 1."""
        test_map = Map()
        test_map.assign_random_images()
        for room in test_map.rooms:
            self.assertTrue("Images/LevelOneMap/" in room.map_image_path)

    def test9_assign_random_images_round2(self):
        """Skipped: Test the assign_random_images method for round 2."""
        test_map = Map()
        test_map.lvl_counter += 1
        test_map.assign_random_images()
        self.skipTest("lvl_counter assigned using GameHandler.counter")
        for room in test_map.rooms:
            self.assertTrue("Images/LevelTwoMap/" in room.map_image_path)

    def test10_print_map(self):
        """Skipped: Test the print_map method."""
        self.skipTest("Don't know how to test for print statements.")
