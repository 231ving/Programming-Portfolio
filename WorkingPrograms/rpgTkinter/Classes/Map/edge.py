"""Module for the Edge class.
"""
import math


class Edge:
    """Class to show how two rooms are related.
    """
    def __init__(self, room1, room2):
        """Creates an edge between two rooms.
        Args:
            room1 (Room): The first room.
            room2 (Room): The second room.
        """
        self.rooms = (room1, room2)
        self.weight = math.dist(room1.get_coordinates(),
                                room2.get_coordinates())

    def get_weight(self):
        """Getter for the edge weight.
        Returns:
            weight (float): The edge weight.
        """
        return self.weight

    def __repr__(self):
        """The representation of the edge.
        Returns:
            str: The string representing two connected rooms and their
             edge weight.
        """
        return f"{self.rooms[0]} <-> {self.rooms[1]} | {self.weight}"
