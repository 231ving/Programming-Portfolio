"""Module containing the unittests for the Edge class.
"""
import unittest
import math
from Classes.Map.edge import Edge
from Classes.Rooms.combat_room import CombatRoom


class EdgeTests(unittest.TestCase):
    """Testcase for the Edge class.
    """
    def test1(self):
        """Test that the Edge instance is made correctly.
        """
        room1 = CombatRoom()
        room1.set_coordinates(5, 10)
        room2 = CombatRoom()
        room2.set_coordinates(10, 5)
        edge = Edge(room1, room2)
        self.assertEqual(edge.rooms, (room1, room2))
        self.assertEqual(edge.weight, math.dist(room1.get_coordinates(), room2.get_coordinates()))

    def test2(self):
        """Test for the get_weight method.
        """
        room1 = CombatRoom()
        room1.set_coordinates(5, 10)
        room2 = CombatRoom()
        room2.set_coordinates(10, 5)
        edge = Edge(room1, room2)
        self.assertTrue(edge.get_weight())

    def test3(self):
        """Test for the __repr__ method.
        """
        room1 = CombatRoom()
        room1.set_coordinates(5, 10)
        room2 = CombatRoom()
        room2.set_coordinates(10, 5)
        edge = Edge(room1, room2)
        x = repr(edge)
        self.assertEqual(x, f"{room1} <-> {room2} | {edge.weight}")
